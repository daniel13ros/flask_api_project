class Task:
    def __init__(self, uuid, title, description, completed=False):
        self.uuid = uuid
        self.title = title
        self.description = description
        self.completed = completed

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }