from DB.db import db
from bson import ObjectId
from bson.errors import InvalidId
from services.log_service import LogService
from utils.validators import Validator  
from utils.errors import ResourceNotFound, ValidationError, DatabaseError

class UserService:

    @staticmethod
    def create_user(user_data):
        email = user_data.get('email')
        Validator.validate_email(email)
        
        username = user_data.get('username')
        Validator.validate_username(username)
        
        if db.users.find_one({"email": email}):
            raise ValidationError("There is already a user with that email")
        
        if db.users.find_one({"username":username}):
            raise ValidationError("There is already a user with that username")
        
        try:
            result = db.users.insert_one(user_data)
            return str(result.inserted_id)
        except Exception as e:
            raise DatabaseError(f"Failed to create user: {str(e)}")

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = db.users.find_one({"_id": ObjectId(user_id)})
            if not user:
                raise ResourceNotFound("User", user_id)
            return user
        except InvalidId:
            raise ValidationError("Invalid User ID format")

    @staticmethod
    def update_user(user_id, update_data):
        if not update_data:
            raise ValidationError("No data provided for update")
        
        try:
            result = db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )

            if result.matched_count == 0:
                raise ResourceNotFound("User", user_id)

            LogService.add_log("USER_UPDATED", f"User {user_id} was updated")
            return True
            
        except InvalidId:
            raise ValidationError("Invalid User ID format")

    @staticmethod
    def delete_user(user_id):
        try:
            result = db.users.delete_one({"_id": ObjectId(user_id)})
            
            if result.deleted_count == 0:
                raise ResourceNotFound("User", user_id)
            
            LogService.add_log("USER_DELETED", f"User {user_id} was deleted")
            return True
            
        except InvalidId:
            raise ValidationError("Invalid User ID format")