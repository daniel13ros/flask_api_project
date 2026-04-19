from DB.db import db
from bson import ObjectId
from bson.errors import InvalidId
from services.log_service import LogService
from utils.validators import Validator
from utils.errors import ResourceNotFound, ValidationError, DatabaseError

class CategoryService:

    @staticmethod
    def create_category(name):
        try:
            Validator.validate_category_name(name)
            
            if db.categories.find_one({"name": name}):
                LogService.add_log("CATEGORY_CREATE_FAILED", f"Attempted to create duplicate category: {name}")
                raise ValidationError("Category with this name already exists")

            result = db.categories.insert_one({"name": name})
            LogService.add_log("CATEGORY_CREATED", f"Category '{name}' created with ID: {result.inserted_id}")
            return str(result.inserted_id)

        except ValidationError as e:
            raise e
        except Exception as e:
            LogService.add_log("CATEGORY_CREATE_ERROR", f"System error creating category '{name}': {str(e)}")
            raise DatabaseError(f"Failed to create category: {str(e)}")

    @staticmethod
    def get_all_categories():
        try:
            return list(db.categories.find())
        except Exception as e:
            LogService.add_log("CATEGORY_GET_ALL_ERROR", f"Error fetching all categories: {str(e)}")
            raise DatabaseError("Failed to fetch categories")

    @staticmethod
    def get_category_by_id(category_id):
        try:
            category = db.categories.find_one({"_id": ObjectId(category_id)})
            if not category:
                LogService.add_log("CATEGORY_GET_FAILED", f"Category {category_id} not found")
                raise ResourceNotFound("Category", category_id)
            return category
        except InvalidId:
            LogService.add_log("CATEGORY_GET_FAILED", f"Invalid Category ID format: {category_id}")
            raise ValidationError("Invalid Category ID format")

    @staticmethod
    def update_category(category_id, new_name):
        try:
            Validator.validate_category_name(new_name)
            
            # בדיקה אם קיים כבר שם כזה לקטגוריה אחרת
            if db.categories.find_one({"name": new_name, "_id": {"$ne": ObjectId(category_id)}}):
                LogService.add_log("CATEGORY_UPDATE_FAILED", f"Attempted to rename category to existing name: {new_name}")
                raise ValidationError("Category name already exists")

            result = db.categories.update_one(
                {"_id": ObjectId(category_id)},
                {"$set": {"name": new_name}}
            )

            if result.matched_count == 0:
                LogService.add_log("CATEGORY_UPDATE_FAILED", f"Category {category_id} not found for update")
                raise ResourceNotFound("Category", category_id)

            LogService.add_log("CATEGORY_UPDATED", f"Category {category_id} renamed to {new_name}")
            return True
            
        except (ValidationError, ResourceNotFound) as e:
            raise e
        except InvalidId:
            LogService.add_log("CATEGORY_UPDATE_FAILED", f"Invalid ID format: {category_id}")
            raise ValidationError("Invalid Category ID format")
        except Exception as e:
            LogService.add_log("CATEGORY_UPDATE_ERROR", f"Error updating category {category_id}: {str(e)}")
            raise DatabaseError(f"Failed to update category: {str(e)}")

    @staticmethod
    def delete_category(category_id):
        try:
            result = db.categories.delete_one({"_id": ObjectId(category_id)})
            
            if result.deleted_count == 0:
                LogService.add_log("CATEGORY_DELETE_FAILED", f"Category {category_id} not found for deletion")
                raise ResourceNotFound("Category", category_id)
            
            LogService.add_log("CATEGORY_DELETED", f"Category {category_id} deleted")
            return True
            
        except InvalidId:
            LogService.add_log("CATEGORY_DELETE_FAILED", f"Invalid ID format: {category_id}")
            raise ValidationError("Invalid Category ID format")
        except Exception as e:
            LogService.add_log("CATEGORY_DELETE_ERROR", f"System error deleting category {category_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete category: {str(e)}")