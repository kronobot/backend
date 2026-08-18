from uuid import UUID


class InscriptionNotFoundException(Exception):
    def __init__(self, id: UUID):
        super().__init__(f"Could not find inscription with ID {id}")
