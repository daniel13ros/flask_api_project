from datetime import datetime
from bson import ObjectId
from typing import List, Optional

class Task:
    def __init__(self, title: str, user_id: ObjectId,description: str = "", status: str = "pending",priority: int = 3,due_date: Optional[datetime] = None,category_id: Optional[ObjectId] = None,subtasks: List = None, _id: Optional[ObjectId] = None,updated_at: Optional[datetime] = None):
        self.id = _id 
        self.user_id = user_id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.category_id = category_id
        self.subtasks = subtasks or []
        self.updated_at = updated_at or datetime.timezone.utc.now()

    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return None
        return cls(
            title=data.get('title'),
            user_id=data.get('user_id'),
            description=data.get('description'),
            status=data.get('status'),
            priority=data.get('priority'),
            due_date=data.get('due_date'),
            category_id=data.get('category_id'),
            subtasks=data.get('subtasks'),
            _id=data.get('_id'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self):
        return {
            'id': str(self.id) if self.id else None, 
            'user_id': str(self.user_id),
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'category_id': str(self.category_id) if self.category_id else None,
            'subtasks': self.subtasks, 
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }