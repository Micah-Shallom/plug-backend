from flask import Flask, jsonify
from config import Config
from flask_migrate import Migrate

from logging.handlers import RotatingFileHandler 
import logging
from app.extensions import db, jwt


def create_app(config_class=Config):
    #imports
    from app.users import user_bp
    from app.jwt_auth import auth_bp

    app = Flask(__name__)
    app.config.from_object(config_class)

    #Initialize Flask extensions here
    db.init_app(app)
    migrate = Migrate(db=db, render_as_batch=True)
    migrate.init_app(app=app)
    jwt.init_app(app)


    # Configure logging
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)  # Set the logging level to ERROR
    app.logger.addHandler(handler)

    # Suppress INFO messages for SQLAlchemy and Alembic
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
    logging.getLogger('alembic').setLevel(logging.ERROR)

    #Register blueprints here
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    #additional claims
    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        #query for more additional claims if the logged in user is admin

        admin_list = ["micahshallom","graceigbadun"]

        if identity in admin_list:
            return {"is_admin":True}
        return {"is_admin": False}

    #jwt error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({
            "message":"Token has expired",
            "error":"token_expired"
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "message":"Signature verification failed",
            "error":"invalid_token"
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "message": "Request doesnt contain valid token",
            "error": "authorization_error"
        }), 401

    return app


from app.models import userAuthModel


