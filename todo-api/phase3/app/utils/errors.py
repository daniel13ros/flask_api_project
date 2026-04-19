class AppError(Exception):
    def __init__(self, message, status_code=400,payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload
        
class ResourceNotFound(AppError):
    def __init__(self, resource_name, resource_id):
        message = f"Resource {resource_name} with ID {resource_id} not found"
        super().__init__(message, status_code=404)

class ValidationError(AppError):
    def __init__(self, message="Invalid data"):
        super().__init__(message, status_code=422)

class DatabaseError(AppError):
    def __init__(self, message="Error communicating with the database"):
        super().__init__(message, status_code=500)