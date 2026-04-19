from DB.db import db
from bson import ObjectId
from bson.errors import InvalidId
from services.log_service import LogService
from utils.validators import Validator  
from utils.errors import ResourceNotFound, ValidationError, DatabaseError
import bcrypt

class UserService:

    @staticmethod
    def create_user(user_data):
        email = user_data.get('email')
        username = user_data.get('username')
        password = user_data.get('password') 
        
        try:
            Validator.validate_email(email)
            Validator.validate_username(username)
            
            if db.users.find_one({"email": email}):
                raise ValidationError("There is already a user with that email")
            
            if db.users.find_one({"username": username}):
                raise ValidationError("There is already a user with that username")
            
            if not password:
                raise ValidationError("Password is required")
                
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_data['password'] = hashed_password.decode('utf-8') 
            
            result = db.users.insert_one(user_data)
            user_id = str(result.inserted_id)
            
            LogService.add_log("USER_CREATED", f"User {user_id} created successfully")
            return user_id
            
        except ValidationError as e:
            LogService.add_log("USER_CREATE_FAILED", f"Validation error for user {username}: {str(e)}")
            raise e
        except Exception as e:
            LogService.add_log("USER_CREATE_ERROR", f"System error creating user: {str(e)}")
            raise DatabaseError(f"Failed to create user: {str(e)}")

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = db.users.find_one({"_id": ObjectId(user_id)})
            if not user:
                LogService.add_log("USER_GET_FAILED", f"User {user_id} not found")
                raise ResourceNotFound("User", user_id)
            return user
        except InvalidId:
            LogService.add_log("USER_GET_FAILED", f"Invalid ID format requested: {user_id}")
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
                LogService.add_log("USER_UPDATE_FAILED", f"User {user_id} not found for update")
                raise ResourceNotFound("User", user_id)

            LogService.add_log("USER_UPDATED", f"User {user_id} was updated")
            return True
            
        except InvalidId:
            LogService.add_log("USER_UPDATE_FAILED", f"Invalid ID format for update: {user_id}")
            raise ValidationError("Invalid User ID format")
        except Exception as e:
            LogService.add_log("USER_UPDATE_ERROR", f"Error updating user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to update user: {str(e)}")

    @staticmethod
    def delete_user(user_id):
        try:
            user_oid = ObjectId(user_id)
            
            user = db.users.find_one({"_id": user_oid})
            if not user:
                LogService.add_log("USER_DELETE_FAILED", f"Attempted to delete non-existent user: {user_id}")
                raise ResourceNotFound("User", user_id)
            
            db.tasks.delete_many({"user_id": str(user_oid)})
            db.users.delete_one({"_id": user_oid})
            
            LogService.add_log("USER_DELETED", f"User {user_id} and all tasks were deleted")
            return True
            
        except InvalidId:
            LogService.add_log("USER_DELETE_FAILED", f"Invalid ID format for deletion: {user_id}")
            raise ValidationError("Invalid User ID format")
        except Exception as e:
            LogService.add_log("USER_DELETE_ERROR", f"System error deleting user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete user and tasks: {str(e)}")
        
    @staticmethod
    def get_all_users():
        try:
            users = list(db.users.find())
            return users
        except Exception as e:
            LogService.add_log("USER_GET_ALL_ERROR", f"System error retrieving all users: {str(e)}")
            raise DatabaseError(f"Failed to retrieve users: {str(e)}")