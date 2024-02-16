from flask import Blueprint
# All routes that makes use of the admin_required decorator will be moved 
# here under the admin blueprint

admin_bp = Blueprint("admin",__name__)

#ay route that will fall under this blueprint will be a child of the main lueprint