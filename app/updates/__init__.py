from flask import Blueprint

profileUpdate_bp = Blueprint("profileUpdate", __name__)

from app.updates import profileUpdateRoute, imageUploadRoute