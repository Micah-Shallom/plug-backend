from flask import Blueprint


user_bp = Blueprint('main', __name__)

from app.users import routes
from app.users import schema