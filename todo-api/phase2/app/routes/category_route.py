from flask import Blueprint, request, jsonify
from app.services.category_service import CategoryService

category_bp = Blueprint('categories', __name__, url_prefix='/categories')

@category_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json() or {}
    category_id = CategoryService.create_category(data)
    return jsonify({
        "message": "Category created successfully",
        "id": category_id
    }), 201

@category_bp.route('/user/<user_id>', methods=['GET'])
def get_user_categories(user_id):
    categories = CategoryService.get_user_categories(user_id)
    return jsonify(categories), 200

@category_bp.route('/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    CategoryService.delete_category(category_id)
    return jsonify({"message": "Category deleted successfully"}), 200