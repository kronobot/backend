from uuid import UUID


class EventNotFoundException(Exception):
    def __init__(self, id: UUID):
        super().__init__(f"Could not find event with ID {id}")
