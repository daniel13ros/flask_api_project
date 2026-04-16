from bson import ObjectId
from typing import Optional

class Category:
    def __init__(self, name: str, user_id: ObjectId, color: str = "#000000", _id: Optional[ObjectId] = None):
        self.id = _id
        self.user_id = user_id
        self.name = name
        self.color = color

    @classmethod
    def from_mongo(cls, data: dict):
        if not data: return None
        return cls(
            name=data.get('name'),
            user_id=data.get('user_id'),
            color=data.get('color', "#000000"),
            _id=data.get('_id')
        )

    def to_dict(self):
        return {
            'id': str(self.id) if self.id else None,
            'user_id': str(self.user_id),
            'name': self.name,
            'color': self.color
        }