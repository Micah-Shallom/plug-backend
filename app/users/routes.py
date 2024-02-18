from app.users import user_bp
from flask_jwt_extended import jwt_required, get_jwt
from flask import render_template, request, jsonify
from app.users.schema import UserSchema

@user_bp.route('/')
def index():
    return render_template("index.html")

@user_bp.get("/all")
@jwt_required()
def get_all_users():
    from app.models.userAuthModel import User

    claims = get_jwt()
    if claims.get("is_admin") == True:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=3, type=int)


        users = User.query.paginate(
            page=page,
            per_page=per_page
        )

        result = UserSchema().dump(users, many=True)

        #construct pagination metadata
        pagination_data = {
            "total": users.total,
            "pages": users.page,
            "page": users.page,
            "per_page": users.per_page,
            "has_next": users.has_next,
            "has_prev": users.has_prev
        }


        return jsonify({
            "users":result,
            "pagination": pagination_data
        }), 200
    return jsonify({
        "message": "You are not authorized to access this"
    })