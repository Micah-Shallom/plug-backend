from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.models import User
from app.updates import profileUpdate_bp


@profileUpdate_bp.put("/profile/<string:user_id>")
def update_profile(user_id):
    # get update request from client
    data = request.get_json()

    #query the database for specfic user to update information
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error":"User not found"}), 404
    
    #update user info as long as it is povided
    # user.fullname = data.get("fullname", user.fullname)
    user.bio = data.get("bio", user.bio)
    user.profile_picture = data.get("profile_picture", user.profile_picture)
    user.phone_number = data.get("phone_number", user.phone_number)
    user.secondary_email = data.get("secondary_email", user.secondary_email)

