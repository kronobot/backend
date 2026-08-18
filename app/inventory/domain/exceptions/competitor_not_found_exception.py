from uuid import UUID


class CompetitorNotFoundException(Exception):
    def __init__(self, id: UUID):
        super().__init__(f"Could not find competitor with ID {id}")
