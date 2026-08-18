from uuid import UUID


class EventTimelineItemNotFoundException(Exception):
    def __init__(self, id: UUID):
        super().__init__(f"Could not find event timeline item with ID {id}")
