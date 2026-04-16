from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId
from pydantic import ValidationError as PydanticError

from app.DB.database import Database
from app.models.task import Task
from app.utils.errors import ResourceNotFound, ValidationError, DatabaseError
from app.utils.validation import TaskCreateSchema 

class TaskService:
    collection_name = "tasks"

    @classmethod
    def _get_collection(cls):
        return Database.get_collection(cls.collection_name)

    @classmethod
    def create_task(cls, task_data: dict) -> str:
        try:
            validated_data = TaskCreateSchema(**task_data)
            task_dict = validated_data.model_dump()

            task_dict['user_id'] = ObjectId(task_dict['user_id'])
            
            if task_dict.get('category_id'):
                cat_id = ObjectId(task_dict['category_id'])
                category = Database.get_collection("categories").find_one({
                    "_id": cat_id, 
                    "user_id": task_dict['user_id']
                })
                if not category:
                    raise ResourceNotFound("Category", str(cat_id))
                task_dict['category_id'] = cat_id

            task_dict['created_at'] = datetime.now(timezone.utc)
            task_dict['updated_at'] = task_dict['created_at']

            result = cls._get_collection().insert_one(task_dict)
            return str(result.inserted_id)

        except InvalidId:
            raise ValidationError("Invalid ID format for user or category")
        except PydanticError as e:
            raise ValidationError(message="Invalid task data", payload=e.errors())
        except Exception as e:
            if isinstance(e, (ValidationError, ResourceNotFound)): raise e
            raise DatabaseError(f"Error creating task: {str(e)}")

    @classmethod
    def get_all_tasks(cls, user_id: str):
        try:
            cursor = cls._get_collection().find({"user_id": ObjectId(user_id)})
            return [Task.from_mongo(task).to_dict() for task in cursor]
        except InvalidId:
            raise ValidationError("Invalid User ID format")
        except Exception as e:
            if isinstance(e, ValidationError): raise e
            raise DatabaseError(f"Error fetching tasks: {str(e)}")

    @classmethod
    def get_task_by_id(cls, task_id: str) -> Task:
        try:
            task_data = cls._get_collection().find_one({"_id": ObjectId(task_id)})
            if not task_data:
                raise ResourceNotFound("Task", task_id)
            return Task.from_mongo(task_data)
        except InvalidId:
            raise ValidationError("Invalid Task ID format")
        except Exception as e:
            if isinstance(e, (ResourceNotFound, ValidationError)): raise e
            raise DatabaseError(f"Error fetching task: {str(e)}")

    @classmethod
    def update_task(cls, task_id: str, update_data: dict):
        try:
            if not update_data:
                raise ValidationError("Data for update cannot be empty")
            
            update_data.pop('_id', None)
            update_data.pop('user_id', None)
            
            update_data['updated_at'] = datetime.now(timezone.utc)
            
            if 'category_id' in update_data and update_data['category_id']:
                update_data['category_id'] = ObjectId(update_data['category_id'])

            result = cls._get_collection().update_one(
                {"_id": ObjectId(task_id)},
                {"$set": update_data}
            )

            if result.matched_count == 0:
                raise ResourceNotFound("Task", task_id)
            
            return True
        except InvalidId:
            raise ValidationError("Invalid ID format in request")
        except Exception as e:
            if isinstance(e, (ResourceNotFound, ValidationError)): raise e
            raise DatabaseError(f"Error updating task: {str(e)}")

    @classmethod
    def delete_task(cls, task_id: str):
        try:
            result = cls._get_collection().delete_one({"_id": ObjectId(task_id)})
            if result.deleted_count == 0:
                raise ResourceNotFound("Task", task_id)
            return True
        except InvalidId:
            raise ValidationError("Invalid Task ID format")
        except Exception as e:
            if isinstance(e, (ResourceNotFound, ValidationError)): raise e
            raise DatabaseError(f"Error deleting task: {str(e)}")