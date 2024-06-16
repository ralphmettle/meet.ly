from flask import Flask, render_template, request
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

def debug_config():
    return True

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'

    from views import config_views
    config_views(app, db, Bcrypt(app))
    
    db.init_app(app)
    migrate = Migrate(app, db)

    return app