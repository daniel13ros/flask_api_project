from flask import Blueprint, request, jsonify
from services.category_service import CategoryService
from utils.errors import ValidationError

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/categories/<category_id>', methods=['GET'])
def get_one(category_id):
    category = CategoryService.get_category_by_id(category_id)
    category['_id'] = str(category['_id'])
    return jsonify({"category": category}), 200

@category_bp.route('/categories', methods=['GET'])
def get_all():
    categories = CategoryService.get_all_categories()
    for cat in categories:
        cat['_id'] = str(cat['_id'])
    return jsonify({"categories": categories}), 200

@category_bp.route('/categories', methods=['POST'])
def create():
    data = request.get_json()
    
    if not data or 'name' not in data or not data['name'].strip():
        return jsonify({"error": "Category name is required"}), 400
        
    cat_id = CategoryService.create_category(data['name'])
    return jsonify({"message": "Category created", "id": cat_id}), 201

@category_bp.route('/categories/<category_id>', methods=['PUT'])
def update(category_id):
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Name field is required for update"}), 400
        
    CategoryService.update_category(category_id, data['name'])
    return jsonify({"message": "Category updated"}), 200

@category_bp.route('/categories/<category_id>', methods=['DELETE'])
def delete(category_id):
    CategoryService.delete_category(category_id)
    return jsonify({"message": "Category deleted"}), 200