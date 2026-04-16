from bson import ObjectId
from bson.errors import InvalidId 
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from app.DB.database import Database
from app.models.user import User
from app.utils.errors import ValidationError, ResourceNotFound, DatabaseError
from app.utils.validation import UserCreateSchema
from pydantic import ValidationError as PydanticError

class UserService:
    collection_name = "users"

    @classmethod
    def create_user(cls, user_data: dict):
        try:
            validated_data = UserCreateSchema(**user_data)
            
            existing_user = Database.get_collection(cls.collection_name).find_one({"email": validated_data.email})
            if existing_user:
                raise ValidationError("User with this email already exists")

            hashed_password = generate_password_hash(validated_data.password)

            new_user = {
                "username": validated_data.username,
                "email": validated_data.email,
                "password_hash": hashed_password,
                "created_at": datetime.now(timezone.utc)
            }

            result = Database.get_collection(cls.collection_name).insert_one(new_user)
            return str(result.inserted_id)

        except PydanticError as e:
            raise ValidationError(message="User data is invalid", payload=e.errors())
        except Exception as e:
            if isinstance(e, ValidationError): raise e
            raise DatabaseError(f"Error creating user: {str(e)}")

    @classmethod
    def get_user_by_id(cls, user_id):
        try:
            u_id = ObjectId(user_id) 
            user_data = Database.get_collection(cls.collection_name).find_one({"_id": u_id})
            if not user_data:
                raise ResourceNotFound("User", user_id)
            return User.from_mongo(user_data)
        except InvalidId:
            raise ValidationError("Invalid User ID format")
        except Exception as e:
            if isinstance(e, (ResourceNotFound, ValidationError)): raise e
            raise DatabaseError(f"Error fetching user: {str(e)}")
    
    
    @classmethod
    def update_user(cls, user_id: str, update_data: dict):
        try:
            if not update_data:
                raise ValidationError("Data for update cannot be empty")

            u_id = ObjectId(user_id)

            update_data.pop('_id', None)
            update_data.pop('email', None) 
            update_data.pop('created_at', None)

            if 'password' in update_data:
                update_data['password_hash'] = generate_password_hash(update_data.pop('password'))

            update_data['updated_at'] = datetime.now(timezone.utc)

            result = Database.get_collection(cls.collection_name).update_one(
                {"_id": u_id},
                {"$set": update_data}
            )

            if result.matched_count == 0:
                raise ResourceNotFound("User", user_id)

            return True

        except InvalidId:
            raise ValidationError("Invalid User ID format")
        except Exception as e:
            if isinstance(e, (ResourceNotFound, ValidationError)): raise e
            raise DatabaseError(f"Error updating user: {str(e)}")
    
    @classmethod
    def delete_user(cls, user_id: str):
        try:
            u_id = ObjectId(user_id)
            
            user = Database.get_collection(cls.collection_name).find_one({"_id": u_id})
            if not user:
                raise ResourceNotFound("User", user_id)

            tasks_result = Database.get_collection("tasks").delete_many({"user_id": u_id})
            categories_result = Database.get_collection("categories").delete_many({"user_id": u_id})

            Database.get_collection(cls.collection_name).delete_one({"_id": u_id})

            return {
                "deleted_user": True,
                "deleted_tasks_count": tasks_result.deleted_count,
                "deleted_categories_count": categories_result.deleted_count
            }

        except InvalidId:
            raise ValidationError("Invalid User ID format")
        except Exception as e:
            if isinstance(e, ResourceNotFound): raise e
            raise DatabaseError(f"Error deleting user: {str(e)}")