from DB.db import db
from bson import ObjectId
from bson.errors import InvalidId
from services.log_service import LogService
from utils.validators import Validator
from utils.errors import ResourceNotFound, ValidationError, DatabaseError

class TaskService:

    @staticmethod
    def get_all_tasks():
        if db.tasks.count_documents({}) == 0:
            raise ResourceNotFound("Task", "all")
        
        return list(db.tasks.find())

    @staticmethod
    def get_task_by_id(task_id):
        try:
            task = db.tasks.find_one({"_id": ObjectId(task_id)})
            if not task:
                raise ResourceNotFound("Task", task_id)
            return task
        except InvalidId:
            raise ValidationError("Invalid Task ID format")

    @staticmethod
    def create_task(data):
        Validator.validate_task_data(data)
        
        data['title'] = Validator.sanitize_input(data.get('title'))
        
        try:
            result = db.tasks.insert_one(data)
            LogService.add_log("TASK_CREATED", f"Task {result.inserted_id} was created")
            return str(result.inserted_id)
        except Exception as e:
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
                raise ResourceNotFound("Task", task_id)

            LogService.add_log("TASK_UPDATED", f"Task {task_id} was updated")
            return True
        except InvalidId:
            raise ValidationError("Invalid Task ID format")

    @staticmethod
    def delete_task(task_id):
        try:
            result = db.tasks.delete_one({"_id": ObjectId(task_id)})
            
            if result.deleted_count == 0:
                raise ResourceNotFound("Task", task_id)
            
            LogService.add_log("TASK_DELETED", f"Task {task_id} was deleted")
            return True
        except InvalidId:
            raise ValidationError("Invalid Task ID format")