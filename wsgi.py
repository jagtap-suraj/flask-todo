from app import app, db
from flask_migrate import upgrade

# Handle database migrations
with app.app_context():
    upgrade()

if __name__ == "__main__":
    app.run()
