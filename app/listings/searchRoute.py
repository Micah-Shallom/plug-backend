from flask import request, jsonify
from app.listings import search_bp  # Importing the blueprint instance
from app.models import Product  # Importing the Product model from app.models

@search_bp.get("/")
def search_products():
    try:
        # Get the search query from the request parameters
        query = request.args.get("query")

        if not query:
            # Return 400 Bad Request if no search query is provided
            return jsonify({"error": "No search query provided"}), 400
        
        # Perform full text-search using PostgreSQL full-text search capabilities
        # Titles and descriptions fields are indexed for full-text search
        results = Product.query.filter(
            Product.title.match(query) | Product.description.match(query)
        ).all()

        # Convert search results to JSON format
        search_results = []
        for product in results:
            product_data = {
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'category_id': product.category_id,
                'business_id': product.business_id
            }
            search_results.append(product_data)

        # Return the search results as JSON with a 200 OK status
        return jsonify({"search_results": search_results}), 200
    except Exception as e:
        # Handle any exceptions and return a 500 Internal Server Error response
        return jsonify({"message": str(e)}), 500
