from app import create_app
from flask import Blueprint, jsonify


app = create_app()


auth_bp = Blueprint("auth",__name__)

@auth_bp.post("/register")
def registerUser():
    return jsonify({"message":"User Created"})