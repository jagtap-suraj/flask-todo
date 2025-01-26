# app/routes.py
from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from app.models import Todo
from app.forms import TodoForm

@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['GET', 'POST'])
def add_todo():
    form = TodoForm()
    if form.validate_on_submit():
        todo = Todo(
            title=form.title.data,
            description=form.description.data,
            completed=form.completed.data
        )
        db.session.add(todo)
        db.session.commit()
        flash('Todo added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_todo.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    todo = Todo.query.get_or_404(id)
    form = TodoForm(obj=todo)
    
    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        todo.completed = form.completed.data
        db.session.commit()
        flash('Todo updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_todo.html', form=form, todo=todo)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/api/todos', methods=['GET', 'POST'])
def api_todos():
    if request.method == 'GET':
        todos = Todo.query.order_by(Todo.created_at.desc()).all()
        return jsonify([todo.to_dict() for todo in todos])
    
    if request.method == 'POST':
        data = request.json
        todo = Todo(
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False)
        )
        db.session.add(todo)
        db.session.commit()
        return jsonify(todo.to_dict()), 201