from app.jwt_auth import auth_bp
from flask import request, jsonify

@auth_bp.post("/register")
def registerUser():
    from app.models.userAuthModel import User

    data = request.get_json()

    user  = User.get_user_by_username(username=data.get("username"))

    if user is not None:
        return jsonify({"error":"User already created"}), 400
    
    new_user = User(
        username=data.get("username"),
        email=data.get("email"),
        role= data.get("role"),
    )
    new_user.set_password(data.get("password"))
    new_user.save()

    return jsonify({"message":"User Created"}), 201

