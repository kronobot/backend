from abc import ABC, abstractmethod
from uuid import UUID

from inventory.domain.team import Team
from inventory.domain.repositories.team_criteria import TeamCriteria


class TeamRepository(ABC):
    @abstractmethod
    def save(self, team: Team) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_criteria(self, criteria: TeamCriteria) -> list[Team]:
        raise NotImplementedError

    @abstractmethod
    def find_or_fail_by_id(self, id: UUID) -> Team:
        raise NotImplementedError
