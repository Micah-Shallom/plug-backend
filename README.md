![logo](./plug_logo.jpg)


# PLUG BACKEND

## Overview

PLUG is a proposed platform designed to connect consumers with entrepreneurs, specifically within the context of Ahmadu Bello University. Here's a summary of what PLUG is and what it aims to achieve:

What is PLUG?
PLUG is an innovative platform that aims to bridge the gap between consumers and entrepreneurs within a university setting. It serves as a marketplace where sellers can showcase their products and services, and consumers can easily find what they need.


This project repository is a Flask-based backend API for managing users, products, businesses, and more. It includes functionality for user authentication, role-based access control, and profile updates with Cloudinary for image uploads.

## Features

- User Registration and Authentication
- Role-based Access Control (Admin, Buyer, Seller)
- CRUD operations for Products, Businesses, and Categories
- Profile updates with image uploads using Cloudinary
- Pagination support for listing users
- Full-text search for products

## Technologies Used

- Flask
- SQLAlchemy
- PostgreSQL
- Flask-JWT-Extended
- Cloudinary
- Marshmallow
- Docker

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Docker (optional, for containerization)

### Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/Micah-Shallom/plug-backend.git
    cd plug-backend
    ```

2. **Create a virtual environment and activate it**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**

    Create a `.env` file in the root directory of the project and add the following:

    ```plaintext
    FLASK_APP=run.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/dbname
    CLOUD_NAME=your_cloudinary_cloud_name
    API_KEY=your_cloudinary_api_key
    API_SECRET=your_cloudinary_api_secret
    ```

5. **Run database migrations**

    ```bash
    flask db upgrade
    ```

6. **Run the application**

    ```bash
    flask run
    ```

### Docker Setup

To run the application using Docker, follow these steps:

1. **Build the Docker image**

    ```bash
    docker build -t plug-backend-api .
    ```

2. **Run the Docker container**

    ```bash
    docker run -p 5000:5000 plug-backend-api
    ```

## API Endpoints

### User Authentication

- **Register**

    ```http
    POST /auth/register
    ```

    **Request Body:**

    ```json
    {
        "fullname": "John Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "password",
        "role": "buyer"
    }
    ```

- **Login**

    ```http
    POST /auth/login
    ```

    **Request Body:**

    ```json
    {
        "email": "johndoe@example.com",
        "password": "password"
    }
    ```

### User Management

- **Get All Users (Admin only)**

    ```http
    GET /users/all
    ```

    **Query Parameters:**

    - `page` (default: 1)
    - `per_page` (default: 3)

- **Update User Profile**

    ```http
    PUT /profile/<string:user_id>
    ```

    **Request Body:**

    ```json
    {
        "bio": "New bio",
        "phone_number": "1234567890",
        "secondary_email": "secondary@example.com"
    }
    ```

### Products

- **Search Products**

    ```http
    GET /products/search
    ```

    **Query Parameters:**

    - `query` (search term)

- **Get Products by Seller**

    ```http
    GET /products/seller/<string:seller_id>
    ```v

## Cloudinary Integration

- **Upload Profile Picture**

    ```http
    POST /profile/upload/<string:user_id>
    ```

    **Request Form Data:**

    - `photo` (image file)

## Decorators for Role-based Access Control

- `@admin_required`: Restricts access to admin users.
- `@is_buyer`: Restricts access to buyers.
- `@is_seller`: Restricts access to sellers.

