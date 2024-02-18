from flask import Blueprint

profileUpdate_bp = Blueprint("update", __name__)

from app.updates import imageUploadRoute, profileUpdateRoute