from DB.db import db
from datetime import datetime, timezone

class LogService:
    
    @staticmethod
    def add_log(action, message, level="INFO"):
        log_entry = {
            "action": action,
            "message": message,
            "level": level.upper(),  
            "timestamp": datetime.now(timezone.utc) 
        }
        
        result = db.system_logs.insert_one(log_entry)
        return str(result.inserted_id)

    @staticmethod
    def get_logs(level=None, limit=50):
        query = {}
        if level:
            query["level"] = level.upper()
            
        return list(db.system_logs.find(query).sort("timestamp", -1).limit(limit))