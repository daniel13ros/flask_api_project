from DB.db import db
from bson import ObjectId
from bson.errors import InvalidId
from services.log_service import LogService
from utils.validators import Validator
from utils.errors import ResourceNotFound, ValidationError, DatabaseError

class CategoryService:

    @staticmethod
    def create_category(name):
        Validator.validate_category_name(name)

        if db.categories.find_one({"name": name}):
            raise ValidationError("Category with this name already exists")

        result = db.categories.insert_one({"name": name})
        
        LogService.add_log("CATEGORY_CREATED", f"Category '{name}' created")
        return str(result.inserted_id)

    @staticmethod
    def get_all_categories():
        return list(db.categories.find())

    @staticmethod
    def get_category_by_id(category_id):
        try:
            category = db.categories.find_one({"_id": ObjectId(category_id)})
            if not category:
                raise ResourceNotFound("Category", category_id)
            return category
        except InvalidId:
            raise ValidationError("Invalid Category ID format")

    @staticmethod
    def update_category(category_id, new_name):
        Validator.validate_category_name(new_name)
        
        try:
            if db.categories.find_one({"name": new_name, "_id": {"$ne": ObjectId(category_id)}}):
                raise ValidationError("Category name already exists")

            result = db.categories.update_one(
                {"_id": ObjectId(category_id)},
                {"$set": {"name": new_name}}
            )

            if result.matched_count == 0:
                raise ResourceNotFound("Category", category_id)

            LogService.add_log("CATEGORY_UPDATED", f"Category {category_id} renamed to {new_name}")
            return True
            
        except InvalidId:
            raise ValidationError("Invalid Category ID format")

    @staticmethod
    def delete_category(category_id):
        try:
            result = db.categories.delete_one({"_id": ObjectId(category_id)})
            
            if result.deleted_count == 0:
                raise ResourceNotFound("Category", category_id)
            
            LogService.add_log("CATEGORY_DELETED", f"Category {category_id} deleted")
            return True
            
        except InvalidId:
            raise ValidationError("Invalid Category ID format")