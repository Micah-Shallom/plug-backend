from flask import Blueprint

auth_bp = Blueprint("auth",__name__)

from app.jwt_auth import routes
