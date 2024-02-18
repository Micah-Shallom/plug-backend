from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.models.productModel import Product
from app.models.categoryModel import Category
from app.listings import product_bp
from app.extensions import db
from app.utils.decorators import is_seller

# Endpoint to create a new product listing
@product_bp.post("/create")
@jwt_required()
@is_seller
def create_product():
    data = request.get_json()
    category = Category.query.filter_by(name=data.get("category")).first()

    seller_id = current_user.id
    category_id = category.category_id if category else None
    title = data.get("title")
    description = data.get("description")
    price = data.get("price")

    if not (seller_id and category_id and title and price):
        return jsonify({
            "message": "Missing required fields"
        }), 400
    
    try:
        new_product = Product(
            seller_id=seller_id,
            category_id=category_id,
            title=title,
            description=description,
            price=price
        )

        new_product.save()

        return jsonify({"message": "Product Listing created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to fetch all products
# this endpoint is for homepage display of products either via slideshow or carousel whatever
@product_bp.get("/all")
def get_products():
    try:
        products = Product.query.all()
        product_list = []

        for product in products:
            product_list.append({
                "id": product.product_id,
                "title": product.title,
                "description": product.description,
                "price": product.price,
            })

        return jsonify(product_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint containing paginated product listings
@product_bp.get("/all-paginated")
@jwt_required()
def get_paginated_products():
    #Pagination parameters
    page = request.args.get("page", 1, type=int)
    per_page =  request.args.get("per_page", 10, type=int)

    #Query all products
    products = Product.query.paginate(page=page, per_page=per_page)

    #Return products in json format
    products_data = []
    for product in products:
        products_data.append(
            {
                "id": product.product_id,
                "title": product.title,
                "desc": product.description,
                "price": product.price,
                "category_id": product.category_id
                #more fields to be added
            }
        )
    
    #construct pagination metadata
    pagination_data = {
        "total": products.total,
        "pages": products.page,
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
    product = Product.query.get_or_404(product_id)

    data = {
        "id": product.product_id,
        "title": product.title,
        "description": product.description,
        "price": product.price
    }

    return jsonify({
        "message": "Product fetched successfully",
        "result": data
    }), 200

# Endpoint to update a product listing
@product_bp.put("/update/<string:product_id>")
@jwt_required()
@is_seller
def update_product(product_id):
    data = request.get_json()
    product = Product.query.filter_by(product_id=product_id).first()

    if not product:
        return jsonify({"error": "Product not found"}), 404

    product.title = data.get('title', product.title)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    
    try:
        db.session.commit()
        return jsonify({
            "message": "Product updated successfully"
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to delete a product listing
@product_bp.delete("/delete/<string:product_id>")
@jwt_required()
@is_seller
def delete_listing(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
