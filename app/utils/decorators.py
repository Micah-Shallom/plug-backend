from functools import wraps
from flask_jwt_extended import get_jwt, current_user
from flask import jsonify

def admin_required(fn):
    """
    Decorator to restrict access to endpoints to only admin users.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Get the JWT data from the current token
        user_token_data = get_jwt()
        # Check if the 'is_admin' claim is present and True
        is_admin = user_token_data.get("is_admin", False)

        # If not an admin, return a 403 Forbidden response
        if not is_admin:
            return jsonify({
                "message": "Only admin users can access this endpoint"
            }), 403
        
        # If an admin, proceed to the wrapped function
        return fn(*args, **kwargs)
    return wrapper

def is_buyer(fn):
    """
    Decorator to restrict access to endpoints to only buyer users.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Get the current user's role from the JWT
        userRole = current_user.role

        # If not a buyer, return a 403 Forbidden response
        if userRole != "buyer":
            return jsonify({
                "message": "Only buyers can access this endpoint"
            }), 403
        
        # If a buyer, proceed to the wrapped function
        return fn(*args, **kwargs)
    return wrapper

def is_seller(fn):
    """
    Decorator to restrict access to endpoints to only seller users.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Get the current user's role from the JWT
        userRole = current_user.role

        # If not a seller, return a 403 Forbidden response
        if userRole != "seller":
            return jsonify({
                "message": "Only sellers can access this endpoint"
            }), 403
        
        # If a seller, proceed to the wrapped function
        return fn(*args, **kwargs)
    return wrapper
