from DB.db import db
from bson import ObjectId
from bson.errors import InvalidId
from services.log_service import LogService
from utils.validators import Validator
from utils.errors import ResourceNotFound, ValidationError, DatabaseError

class TaskService:

    @staticmethod
    def get_all_tasks():
        try:
            return list(db.tasks.find())
        except Exception as e:
            LogService.add_log("TASK_GET_ALL_ERROR", f"Error fetching tasks: {str(e)}")
            raise DatabaseError("Failed to fetch tasks")

    @staticmethod
    def get_task_by_id(task_id):
        try:
            task = db.tasks.find_one({"_id": ObjectId(task_id)})
            if not task:
                LogService.add_log("TASK_GET_FAILED", f"Task {task_id} not found")
                raise ResourceNotFound("Task", task_id)
            return task
        except InvalidId:
            LogService.add_log("TASK_GET_FAILED", f"Invalid Task ID format: {task_id}")
            raise ValidationError("Invalid Task ID format")

    @staticmethod
    def get_tasks_by_user_id(user_id):
        try:
            user_oid = ObjectId(user_id)
            if not db.users.find_one({"_id": user_oid}):
                LogService.add_log("TASK_GET_BY_USER_FAILED", f"User {user_id} not found")
                raise ResourceNotFound("User", user_id)
            
            return list(db.tasks.find({"user_id": str(user_oid)}))
        except InvalidId:
            LogService.add_log("TASK_GET_BY_USER_FAILED", f"Invalid User ID format: {user_id}")
            raise ValidationError("Invalid User ID format")

    @staticmethod
    def get_tasks_by_category(category_id):
        try:
            category_oid = ObjectId(category_id)
            if not db.categories.find_one({"_id": category_oid}):
                LogService.add_log("TASK_GET_BY_CAT_FAILED", f"Category {category_id} not found")
                raise ResourceNotFound("Category", category_id)
            
            return list(db.tasks.find({"category_id": str(category_oid)}))
        except InvalidId:
            LogService.add_log("TASK_GET_BY_CAT_FAILED", f"Invalid Category ID format: {category_id}")
            raise ValidationError("Invalid Category ID format")

    @staticmethod
    def create_task(data):
        try:
            Validator.validate_task_data(data)
            data['title'] = Validator.sanitize_input(data.get('title'))
            
            if data.get('user_id') and not db.users.find_one({"_id": ObjectId(data['user_id'])}):
                LogService.add_log("TASK_CREATE_FAILED", f"User {data['user_id']} not found for new task")
                raise ResourceNotFound("User", data['user_id'])

            result = db.tasks.insert_one(data)
            LogService.add_log("TASK_CREATED", f"Task {result.inserted_id} was created")
            return str(result.inserted_id)
            
        except ValidationError as e:
            LogService.add_log("TASK_CREATE_FAILED", f"Validation error: {str(e)}")
            raise e
        except Exception as e:
            LogService.add_log("TASK_CREATE_ERROR", f"System error creating task: {str(e)}")
            raise DatabaseError(f"Failed to create task: {str(e)}")

    @staticmethod
    def update_task(task_id, update_data):
        if not update_data:
            raise ValidationError("No data provided for update")

        try:
            result = db.tasks.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": update_data}
            )

            if result.matched_count == 0:
                LogService.add_log("TASK_UPDATE_FAILED", f"Task {task_id} not found for update")
                raise ResourceNotFound("Task", task_id)

            LogService.add_log("TASK_UPDATED", f"Task {task_id} was updated")
            return True
        except InvalidId:
            LogService.add_log("TASK_UPDATE_FAILED", f"Invalid Task ID format: {task_id}")
            raise ValidationError("Invalid Task ID format")
        except Exception as e:
            LogService.add_log("TASK_UPDATE_ERROR", f"Error updating task {task_id}: {str(e)}")
            raise DatabaseError(f"Failed to update task: {str(e)}")

    @staticmethod
    def delete_task(task_id):
        try:
            result = db.tasks.delete_one({"_id": ObjectId(task_id)})
            
            if result.deleted_count == 0:
                LogService.add_log("TASK_DELETE_FAILED", f"Task {task_id} not found for deletion")
                raise ResourceNotFound("Task", task_id)
            
            LogService.add_log("TASK_DELETED", f"Task {task_id} was deleted")
            return True
        except InvalidId:
            LogService.add_log("TASK_DELETE_FAILED", f"Invalid Task ID format: {task_id}")
            raise ValidationError("Invalid Task ID format")
        except Exception as e:
            LogService.add_log("TASK_DELETE_ERROR", f"System error deleting task {task_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete task: {str(e)}")