from flask import Flask, jsonify
from config import Config
from flask_migrate import Migrate
from app.models.userAuthModel import User, TokenBlockList

from logging.handlers import RotatingFileHandler 
import logging
from app.extensions import db, jwt
from flask_cors import CORS


def create_app(config_class=Config):
    # Import blueprints
    from app.users import user_bp
    from app.jwt_auth import auth_bp
    from app.listings import category_bp, product_bp, seller_bp, search_bp
    from app.updates import profileUpdate_bp
    from app.business import business_bp

    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    # Initialize Flask extensions
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

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(category_bp, url_prefix="/categories")
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(seller_bp, url_prefix="/sellers")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(profileUpdate_bp, url_prefix="/update")
    app.register_blueprint(business_bp, url_prefix="/business")

    # Define JWT user lookup loader
    @jwt.user_lookup_loader
    def user_lookup_callback(__jwt_headers, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(username=identity).one_or_none()

    # Define additional JWT claims loader
    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        # Query for more additional claims if the logged-in user is admin
        admin_list = ["micahshallom", "graceigbadun"]

        if identity in admin_list:
            return {"is_admin": True}
        return {"is_admin": False}

    # Define JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({
            "message": "Token has expired",
            "error": "token_expired"
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "message": "Signature verification failed",
            "error": "invalid_token"
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "message": "Request doesn't contain a valid token",
            "error": "authorization_error"
        }), 401
    
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data['jti']

        token = db.session.query(TokenBlockList).filter(TokenBlockList.jti == jti).scalar()

        return token is not None

    return app

from app.models import userAuthModel
