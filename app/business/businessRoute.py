from flask import request, jsonify
from app.business import business_bp
from flask_jwt_extended import jwt_required, current_user
from app.utils.decorators import is_seller
from app.models.businessModel import Business
from app.models import db

# Endpoint to create a new business
@business_bp.post("/create")
@jwt_required()
@is_seller
def create_business():
    # Extract data from the request JSON
    data = request.get_json()

    # Get the seller's ID from the current user
    seller_id = current_user.id

    try:
        # Create a new Business instance with the provided data
        business = Business(
            name=data.get("name"),
            description=data.get("description"),
            owner_id=seller_id
        )

        # Save the new business to the database
        business.save(commit=True)

        # Return success message
        return jsonify({"message": "Business created successfully"}), 201
    except Exception as e:
        # Return error message if an exception occurs
        return jsonify({"message": str(e)}), 500

# Endpoint to fetch all businesses
@business_bp.get("/all")
def get_all_businesses():
    try:
        # Retrieve all businesses from the database
        businesses = Business.query.all()
        business_list = []

        # Iterate through the businesses and create a list of dictionaries
        for business in businesses:
            business_list.append({
                "id": business.id,
                "name": business.name,
                "description": business.description,
            })

        # Return the list of businesses as JSON
        return jsonify({
            "message": "All businesses fetched",
            "data": business_list
        }), 200
    except Exception as e:
        # Return error message if an exception occurs
        return jsonify({"message": str(e)}), 500

# Endpoint to fetch paginated businesses
@business_bp.get("/all-paginated")
def get_paginated_businesses():
    # Extract pagination parameters from the request
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    try:
        # Paginate the businesses
        businesses = Business.query.paginate(page=page, per_page=per_page)

        business_list = []

        # Iterate through the paginated businesses and create a list of dictionaries
        for business in businesses.items:
            business_list.append({
                "id": business.id,
                "name": business.name,
                "description": business.description,
            })

        # Construct pagination metadata
        pagination_data = {
            "total": businesses.total,
            "pages": businesses.pages,
            "page": businesses.page,
            "per_page": businesses.per_page,
            "has_next": businesses.has_next,
            "has_prev": businesses.has_prev
        }

        # Return paginated businesses and metadata as JSON
        return jsonify({
            "message": "All businesses fetched",
            "data": business_list,
            "pagination_data": pagination_data
        }), 200

    except Exception as e:
        # Return error message if an exception occurs
        return jsonify({"message": str(e)}), 500

# Endpoint to fetch a business by ID
@business_bp.get("/<string:business_id>")
def get_business_by_id(business_id):
    # Query the database for the business with the specified ID
    business = Business.query.filter_by(id=business_id).first_or_404()

    # Create a dictionary containing business data
    business_data = {
        "id": business.id,
        "name": business.name,
        "description": business.description,
    }

    # Return the business data as JSON
    return jsonify({
        "message": "Business fetched successfully",
        "data": business_data
    }), 200

# Endpoint to update a business listing
@business_bp.put("/update/<string:business_id>")
@jwt_required()
@is_seller
def update_business(business_id):
    # Extract data from the request JSON
    data = request.get_json()

    # Query the database for the business to update
    business = Business.query.filter_by(id=business_id).first_or_404()

    if not business:
        # Return error message if the business is not found
        return jsonify({"message": "Business not found"}), 404

    # Update business attributes with the provided data
    business.title = data.get('title', business.name)
    business.description = data.get('description', business.description)

    try:
        # Commit the changes to the database
        db.session.commit()
        # Return success message
        return jsonify({
            "message": "Business updated successfully"
        }), 201
    except Exception as e:
        # Return error message if an exception occurs
        return jsonify({"message": str(e)}), 500

# Endpoint to delete a business listing
@business_bp.delete("/delete/<string:business_id>")
@jwt_required()
@is_seller
def delete_listing(business_id):
    # Query the database for the business to delete
    business = Business.query.get(business_id)
    if not business:
        # Return error message if the business is not found
        return jsonify({'message': 'Business not found'}), 404

#more features/routes
#---------getting products registered under a business
    