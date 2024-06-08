from flask import request, jsonify
from app.models import User
from app.updates import profileUpdate_bp
from flask_jwt_extended import jwt_required

@profileUpdate_bp.put("/profile/<string:user_id>")
@jwt_required()  # Requires JWT authentication for this route
def update_profile(user_id):
    # Get update request data from client
    data = request.get_json()

    # Query the database for the specific user to update information
    user = User.query.filter_by(id=user_id).first()

    # Check if the user exists
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Update user information if provided in the request data
    # user.fullname = data.get("fullname", user.fullname)  # Uncomment if fullname can be updated
    user.bio = data.get("bio", user.bio)
    user.phone_number = data.get("phone_number", user.phone_number)
    user.secondary_email = data.get("secondary_email", user.secondary_email)

    try:
        # Save the updated user profile to the database
        user.save(commit=True)
        return jsonify({"message": "User profile updated successfully"}), 201

    except Exception as e:
        # Handle exception if saving fails
        # user.rollback()  # Uncomment if rollback method is available
        return jsonify({'message': 'Failed to update user profile'}), 500
