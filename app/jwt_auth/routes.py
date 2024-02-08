from app.jwt_auth import auth_bp
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, current_user

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
        password=data.get("password")
    )
    new_user.set_password(data.get("password"))
    new_user.save()

    return jsonify({"message":"User Created"}), 201


@auth_bp.post("/login")
def login_user():
    from app.models.userAuthModel import User

    data = request.get_json()

    user = User.get_user_by_username(username=data.get("username"))

    if user and (user.check_password(password= data.get("password"))):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.password)

        return jsonify(
            {
                "message": "Logged in successfully",
                "tokens":{
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            }
        ), 200

    return jsonify({"error": "Invalid username and password"}), 400

@auth_bp.get('/whoami')
@jwt_required()
def whoami():
    return jsonify({
        "message": "message",
        "user_details":{
            "username": current_user.username,
            "email": current_user.email,
            "role": current_user.role
        }
    })