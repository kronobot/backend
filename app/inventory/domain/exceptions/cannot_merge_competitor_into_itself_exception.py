from uuid import UUID


class CannotMergeCompetitorIntoItselfException(Exception):
    def __init__(self, competitor_id: UUID):
        super().__init__(f"Cannot merge competitor {competitor_id} into itself")
