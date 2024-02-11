from functools import wraps
from flask_jwt_extended import get_jwt, current_user
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_token_data = get_jwt()
        is_admin = user_token_data.get("is_admin",False)

        if not is_admin:
            return jsonify({
                "message": "Only admin users can access this endpoint"
            }), 403
        
        return fn(*args, **kwargs)
    return wrapper


def is_buyer(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        userRole = current_user.role

        if userRole != "buyer":
            return jsonify({
                "message": "Only buyers can access this endpoint"
            }), 403
        return fn(*args, **kwargs)
    return wrapper


def is_seller(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        userRole =  current_user.role

        if userRole != "seller":
            return jsonify({
                "message": "Only sellers can access this endpoint"
            }), 403
        return fn(*args, **kwargs)
    return wrapper