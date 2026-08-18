from abc import ABC, abstractmethod
from uuid import UUID

from inventory.domain.stage_result import StageResult
from inventory.domain.repositories.stage_result_criteria import StageResultCriteria


class StageResultRepository(ABC):
    @abstractmethod
    def save(self, stage_result: StageResult) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_criteria(self, criteria: StageResultCriteria) -> list[StageResult]:
        raise NotImplementedError

    @abstractmethod
    def find_or_fail_by_id(self, id: UUID) -> StageResult:
        raise NotImplementedError
