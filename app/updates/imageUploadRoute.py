import cloudinary
import cloudinary.uploader
import cloudinary.api
import logging
import os
from dotenv import load_dotenv
from flask_cors import cross_origin
from flask import jsonify, request
from cloudinary.utils import cloudinary_url
from app import create_app
from app.updates import profileUpdate_bp
from app.models import User

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Flask Blueprint for profile updates
@profileUpdate_bp.post("/upload/<string:user_id>")
@cross_origin()
def upload_file(user_id):
    # Initialize Flask application
    app = create_app()

    # Log Cloudinary configuration information
    app.logger.info('%s', os.getenv('CLOUD_NAME'))
    app.logger.info('in upload route')

    # Configure Cloudinary with environment variables
    cloudinary.config(
        cloud_name=os.getenv('CLOUD_NAME'),
        api_key=os.getenv('API_KEY'),
        api_secret=os.getenv('API_SECRET')
    )

    # Retrieve uploaded file from request
    file_to_upload = request.files['photo']
    app.logger.info('%s file_to_upload', file_to_upload)

    # Define transformation options for image upload
    transformation_options = {
        "width": 300,
        "height": 300,
        "quality": "auto:low"
    }

    if file_to_upload:
        # Upload file to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file_to_upload,
            public_id=user_id,
            folder="plugUsers",
            resource_type="image",
            transformation=transformation_options
        )

        app.logger.info(upload_result)
        app.logger.info(type(upload_result))

        # Retrieve secure URL of the uploaded image
        secure_image_url = upload_result["secure_url"]

        # Update user's profile picture URL in the User database
        user = User.query.filter_by(id=user_id).first()

        if user:
            user.profile_picture = secure_image_url
            try:
                user.save(commit=True)
                return jsonify({
                    "message": "Profile Picture updated successfully",
                    "upload_result": upload_result
                }), 201
            except Exception as e:
                app.logger.error('Failed to update profile picture: %s', str(e))
                return jsonify({'message': 'Failed to update profile picture'}), 500
        else:
            return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"message": "File not uploaded"}), 400

@profileUpdate_bp.post("/cld_optimize")
@cross_origin()
def cld_optimize():
    # Initialize Flask application
    app = create_app()
    app.logger.info('in optimize route')

    # Configure Cloudinary with environment variables
    cloudinary.config(
        cloud_name=os.getenv('CLOUD_NAME'),
        api_key=os.getenv('API_KEY'),
        api_secret=os.getenv('API_SECRET')
    )

    if request.method == 'POST':
        # Retrieve public_id of the image to optimize
        public_id = request.form['public_id']
        app.logger.info('%s public id', public_id)

        if public_id:
            # Generate optimized URL for the image from Cloudinary
            cld_url = cloudinary_url(public_id, fetch_format='auto', quality='auto', secure=True)

            app.logger.info(cld_url)
            return jsonify(cld_url)

