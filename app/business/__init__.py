from flask import Blueprint


business_bp = Blueprint("Business", __name__)

from app.business import businessRoute