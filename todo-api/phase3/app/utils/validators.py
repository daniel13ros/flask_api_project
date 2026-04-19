import re
import html
from utils.errors import ValidationError

class Validator:
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    @staticmethod
    def sanitize_input(data):
        if isinstance(data, str):
            return html.escape(data.strip())
        return data

    @staticmethod
    def validate_email(email):
        if not email or not re.match(Validator.EMAIL_REGEX, email):
            raise ValidationError("Invalid email format")
        return True

    @staticmethod
    def validate_username(username):
        if not username or len(username) < 3 or len(username) > 20:
            raise ValidationError("Username must be between 3 and 20 characters")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores")
        return True

    @staticmethod
    def validate_task_data(data):
        title = data.get('title')
        if not title or len(title) < 3:
            raise ValidationError("Task title must be at least 3 characters long")
        return True

    @staticmethod
    def validate_category_name(name):
        if not name or len(name) < 2:
            raise ValidationError("Category name must be at least 2 characters")
        return True