# app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
from app.models import db

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

# Import routes after app creation to avoid circular imports
from app import routes
