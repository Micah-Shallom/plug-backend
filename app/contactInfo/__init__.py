from flask import Blueprint


contact_bp = Blueprint("contacts", __name__)

from app.contactInfo import contactInfo, payment
