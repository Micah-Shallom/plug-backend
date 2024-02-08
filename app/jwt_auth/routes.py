from app.jwt_auth import auth_bp
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, current_user, get_jwt_identity, get_jwt

@auth_bp.post("/register")
def registerUser():
    from app.models.userAuthModel import User, TokenBlockList

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


@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_accessToken():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    return jsonify({"access_token": new_access_token})

@auth_bp.get("/logout")
@jwt_required(verify_type=False)
def logout_user():
    from app.models.userAuthModel import TokenBlockList

    jwt = get_jwt()
    jti = jwt['jti']
    token_type = jwt["type"]

    token_b = TokenBlockList(jti=jti)

    token_b.save()

    return jsonify({"message":f"{token_type} revoked successfully"}), 200