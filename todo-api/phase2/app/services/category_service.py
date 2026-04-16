from bson import ObjectId
from bson.errors import InvalidId 
from app.DB.database import Database
from app.models.category import Category
from app.utils.errors import ResourceNotFound, ValidationError, DatabaseError
from app.utils.validation import CategorySchema
from pydantic import ValidationError as PydanticError

class CategoryService:
    collection_name = "categories"

    @classmethod
    def create_category(cls, category_data: dict):
        try:
            validated_data = CategorySchema(**category_data)
            cat_dict = validated_data.model_dump()
            
            user_id_obj = ObjectId(cat_dict['user_id'])
            category_name = cat_dict['name']

            user_exists = Database.get_collection("users").find_one({"_id": user_id_obj})
            if not user_exists:
                raise ResourceNotFound("User", str(user_id_obj))

            existing_category = Database.get_collection(cls.collection_name).find_one({
                "user_id": user_id_obj,
                "name": {"$regex": f"^{category_name}$", "$options": "i"} 
            })

            if existing_category:
                raise ValidationError(f"Category with the name '{category_name}' already exists")

            cat_dict['user_id'] = user_id_obj
            result = Database.get_collection(cls.collection_name).insert_one(cat_dict)
            
            return str(result.inserted_id)

        except InvalidId:
            raise ValidationError("Invalid ID format provided")
        except PydanticError as e:
            raise ValidationError(message="Category data is invalid", payload=e.errors())
        except Exception as e:
            if isinstance(e, (ValidationError, ResourceNotFound)): raise e
            raise DatabaseError(f"Error creating category: {str(e)}")

    @classmethod
    def get_user_categories(cls, user_id: str):
        try:
            u_id = ObjectId(user_id)
            cursor = Database.get_collection(cls.collection_name).find({"user_id": u_id})
            return [Category.from_mongo(c).to_dict() for c in cursor]
        except InvalidId:
            raise ValidationError("Invalid User ID format")
        except Exception as e:
            if isinstance(e, ValidationError): raise e
            raise DatabaseError(f"Error fetching categories: {str(e)}")

    @classmethod
    def delete_category(cls, category_id: str):
        try:
            c_id = ObjectId(category_id)
            
            tasks_count = Database.get_collection("tasks").count_documents({"category_id": c_id})
            if tasks_count > 0:
                raise ValidationError("Cannot delete a category that has existing tasks")

            result = Database.get_collection(cls.collection_name).delete_one({"_id": c_id})
            if result.deleted_count == 0:
                raise ResourceNotFound("Category", category_id)
            
            return True
        except InvalidId:
            raise ValidationError("Invalid Category ID format")
        except Exception as e:
            if isinstance(e, (ValidationError, ResourceNotFound)): raise e
            raise DatabaseError(f"Error deleting category: {str(e)}")