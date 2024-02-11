from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt
from flask import jsonify, request
from app.listings import category_bp
from app.models.categoryModel import Category

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


@category_bp.post("/add")
@jwt_required()
@admin_required
def create_category():
    data = request.get_json()

    try:
        new_category = Category(
            name = data.get("name"),
            description = data.get("description")
        )

        new_category.save()

        return jsonify({
            "message":"Category created successfully"
        }), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500
