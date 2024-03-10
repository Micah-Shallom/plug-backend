from flask import request, jsonify
from app.extensions import db
from app.contactInfo import contact_bp
from app.models.contactInfoModel import ContactInfo


# Create a new contact information entry
@contact_bp.route('/contacts', methods=['POST'])
def create_contact_info():
    data = request.get_json()
    new_contact_info = ContactInfo(**data)

    try:
        new_contact_info.save(commit=True)
        return jsonify({"message": "Contact information created successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Get all contact information entries
@contact_bp.route('/contacts', methods=['GET'])
def get_all_contact_info():
    contact_info_list = ContactInfo.query.all()
    result = [contact_info.to_dict() for contact_info in contact_info_list]
    return jsonify(result), 200

# Get a specific contact information entry by ID
@contact_bp.route('/contacts/<string:user_id>', methods=['GET'])
def get_contact_info(user_id):
    contact_info = ContactInfo.query.get_or_404(user_id)
    return jsonify(contact_info.to_dict()), 200

# Update a specific contact information entry by ID
@contact_bp.route('/contacts/<string:user_id>', methods=['PUT'])
def update_contact_info(user_id):
    contact_info = ContactInfo.query.get_or_404(user_id)
    data = request.get_json()

    try:
        for key, value in data.items():
            setattr(contact_info, key, value)
        
        db.session.commit()

        return jsonify({"message": "Contact information updated successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Delete a specific contact information entry by ID
@contact_bp.route('/contacts/<string:user_id>', methods=['DELETE'])
def delete_contact_info(user_id):
    contact_info = ContactInfo.query.get_or_404(user_id)

    try:
        db.session.delete(contact_info)
        db.session.commit()
        return jsonify({"message": "Contact information deleted successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
