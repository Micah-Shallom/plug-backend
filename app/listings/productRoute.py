from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.models.productModel import Product
from app.models.categoryModel import Category
from app.models.businessModel import Business
from app.listings import product_bp
from app.extensions import db
from app.utils.decorators import is_seller

# Endpoint to create a new product listing
@product_bp.post("/create")
@jwt_required()
@is_seller
def create_product():
    data = request.get_json()

    # Fetch the category from the provided data
    category = Category.query.filter_by(name=data.get("category")).first_or_404()
    business = Business.query.filter_by(name=data.get("business")).first()


    # Extract necessary fields from the request data
    seller_id = current_user.id
    category_id = category.id if category else None
    business_id = business.id if business else None
    title = data.get("title")
    description = data.get("description")
    price = data.get("price")

    # Check if all required fields are provided
    if not (seller_id and category_id and title and price):
        return jsonify({
            "message": "Missing required fields"
        }), 400
    
    try:
        # Create a new Product instance
        new_product = Product(
            seller_id=seller_id,
            category_id=category_id,
            business_id = business_id,
            title=title,
            description=description,
            price=price
        )

        # Save the new product to the database
        new_product.save(commit=True)

        return jsonify({"message": "Product Listing created successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Endpoint to fetch all products
@product_bp.get("/all")
def get_products():
    try:
        # Retrieve all products from the database
        products = Product.query.all()
        product_list = []

        # Construct a list of product dictionaries
        for product in products:
            product_list.append({
                "id": product.id,
                "title": product.title,
                "description": product.description,
                "price": product.price,
            })

        # Return the list of products as JSON
        return jsonify({
            "message": "All products fetched",
            "data": product_list
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Endpoint containing paginated product listings
@product_bp.get("/all-paginated")
@jwt_required()
def get_paginated_products():
    # Pagination parameters
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # Query all products with pagination
    products = Product.query.paginate(page=page, per_page=per_page)

    # Construct JSON response for paginated products
    products_data = []
    for product in products.items:
        products_data.append(
            {
                "id": product.id,
                "title": product.title,
                "description": product.description,
                "price": product.price,
                "category_id": product.category_id
                # More fields can be added
            }
        )
    
    # Construct pagination metadata
    pagination_data = {
        "total": products.total,
        "pages": products.pages,
        "page": products.page,
        "per_page": products.per_page,
        "has_next": products.has_next,
        "has_prev": products.has_prev
    }

    return jsonify({
        "products": products_data,
        "pagination": pagination_data
    }), 200

# Endpoint to fetch a product listing by its id
@product_bp.get("/<string:product_id>")
def get_product_by_id(product_id):
    # Query the database for the product with the specified ID
    product = Product.query.get_or_404(product_id)

    # Create a dictionary containing product data
    product_data = {
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "price": product.price
    }

    # Return the product data as JSON
    return jsonify({
        "message": "Product fetched successfully",
        "data": product_data
    }), 200

# Endpoint to update a product listing
@product_bp.put("/update/<string:product_id>")
@jwt_required()
@is_seller
def update_product(product_id):
    data = request.get_json()

    # Query the database for the product to update
    product = Product.query.filter_by(id=product_id).first_or_404()

    if not product:
        return jsonify({"message": "Product not found"}), 404

    # Update product attributes with the provided data
    product.title = data.get('title', product.title)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    
    try:
        # Commit the changes to the database
        db.session.commit()
        return jsonify({
            "message": "Product updated successfully"
        }), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Endpoint to delete a product listing
@product_bp.delete("/delete/<string:product_id>")
@jwt_required()
@is_seller
def delete_listing(product_id):
    # Query the database for the product to delete
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404


#==========TO ADD=================
"""
    Ability to Query Products based on businesses
"""