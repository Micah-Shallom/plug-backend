from flask import Blueprint


contact_bp = Blueprint("contacts", __name__)
payment_bp = Blueprint("payments", __name__)

from app.contactInfo import contactInfo, payment
