from uuid import UUID


class NotificationTaskNotFoundException(Exception):
    def __init__(self, id: UUID):
        super().__init__(f"Could not find notification task with ID {id}")
