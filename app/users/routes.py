from app.users import user_bp
from flask_jwt_extended import jwt_required, get_jwt
from flask import render_template, request, jsonify
from app.users.schema import UserSchema

@user_bp.route('/')
def index():
    """
    Route to render the index.html template.
    """
    return render_template("index.html")

@user_bp.get("/all")
@jwt_required()
def get_all_users():
    """
    Route to fetch all users with pagination, accessible only to admins.
    Requires JWT authentication with 'is_admin' claim.
    """
    from app.models.userAuthModel import User  # Import User model here (assuming it's from userAuthModel)

    # Retrieve claims from JWT token
    claims = get_jwt()

    # Check if user is an admin
    if claims.get("is_admin") == True:
        # Retrieve pagination parameters from query parameters
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=3, type=int)

        # Query users with pagination
        users = User.query.paginate(
            page=page,
            per_page=per_page
        )

        # Serialize users data using UserSchema
        result = UserSchema().dump(users, many=True)

        # Construct pagination metadata
        pagination_data = {
            "total": users.total,
            "pages": users.pages,
            "page": users.page,
            "per_page": users.per_page,
            "has_next": users.has_next,
            "has_prev": users.has_prev
        }

        # Return JSON response with users data and pagination metadata
        return jsonify({
            "users": result,
            "pagination": pagination_data
        }), 200
    else:
        # Return unauthorized message if user is not an admin
        return jsonify({
            "message": "You are not authorized to access this"
        }), 403
