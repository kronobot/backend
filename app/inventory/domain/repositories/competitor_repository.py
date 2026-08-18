from abc import ABC, abstractmethod
from uuid import UUID

from inventory.domain.competitor import Competitor
from inventory.domain.repositories.competitor_criteria import CompetitorCriteria


class CompetitorRepository(ABC):
    @abstractmethod
    def save(self, competitor: Competitor) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_criteria(self, criteria: CompetitorCriteria) -> list[Competitor]:
        raise NotImplementedError

    @abstractmethod
    def find_or_fail_by_id(self, id: UUID) -> Competitor:
        raise NotImplementedError

    @abstractmethod
    def delete(self, competitor: Competitor) -> None:
        raise NotImplementedError
