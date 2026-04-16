from datetime import datetime
from bson import ObjectId
from typing import Optional

class User:
    def __init__(self, username: str, email: str, password_hash: str, _id: Optional[ObjectId] = None, created_at: Optional[datetime] = None):
        self.id = _id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.timezone.utc.now()
        
    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return None
        return cls(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            _id=data.get('_id'),
            created_at=data.get('created_at')
        )
    
    def to_dict(self , include_password=False):
        user_dict = {
            'id': str(self.id) if self.id else None,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_password:
            user_dict['password_hash'] = self.password_hash
        return user_dict