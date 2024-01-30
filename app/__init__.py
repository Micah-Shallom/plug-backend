from flask import Flask
from config import Config
from flask_migrate import Migrate

from logging.handlers import RotatingFileHandler 
import logging
from app.extensions import db


def create_app(config_class=Config):
    #imports
    from app.main import bp as main_bp
    from app.jwt_auth import auth_bp as abp

    app = Flask(__name__)
    app.config.from_object(config_class)

    #Initialize Flask extensions here
    db.init_app(app)
    migrate = Migrate(db=db, render_as_batch=True)
    migrate.init_app(app=app)


    # Configure logging
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)  # Set the logging level to ERROR
    app.logger.addHandler(handler)

    # Suppress INFO messages for SQLAlchemy and Alembic
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
    logging.getLogger('alembic').setLevel(logging.ERROR)

    #Register blueprints here
    app.register_blueprint(main_bp)
    app.register_blueprint(abp, url_prefix="/auth")
    
    return app

from app.models import userAuthModel


