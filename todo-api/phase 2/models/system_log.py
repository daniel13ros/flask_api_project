from datetime import datetime
from typing import Optional

class SystemLog:
    def __init__(self, level: str, message: str, endpoint: str, traceback: Optional[str] = None, user_id: Optional[str] = None):
        self.timestamp = datetime.timezone.utc.now()
        self.level = level
        self.message = message
        self.endpoint = endpoint
        self.traceback = traceback
        self.user_id = user_id

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'level': self.level,
            'message': self.message,
            'endpoint': self.endpoint,
            'traceback': self.traceback,
            'user_id': self.user_id
        }