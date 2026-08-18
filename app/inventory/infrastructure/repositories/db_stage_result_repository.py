from uuid import UUID

from inventory.domain.stage_result import StageResult
from inventory.domain.exceptions.stage_result_not_found_exception import StageResultNotFoundException
from inventory.domain.repositories.stage_result_criteria import StageResultCriteria
from inventory.domain.repositories.stage_result_repository import StageResultRepository


class DbStageResultRepository(StageResultRepository):
    def save(self, stage_result: StageResult) -> None:
        stage_result.save()

    def find_by_criteria(self, criteria: StageResultCriteria) -> list[StageResult]:
        queryset = StageResult.objects.all()

        if criteria.id is not None:
            queryset = queryset.filter(id=criteria.id)
        if criteria.inscription is not None:
            queryset = queryset.filter(inscription_id=criteria.inscription)
        if criteria.event_stage is not None:
            queryset = queryset.filter(event_stage_id=criteria.event_stage)
        if criteria.value_seconds is not None:
            queryset = queryset.filter(value_seconds=criteria.value_seconds)
        if criteria.rank is not None:
            queryset = queryset.filter(rank=criteria.rank)

        return list(queryset)

    def find_or_fail_by_id(self, id: UUID) -> StageResult:
        try:
            return StageResult.objects.get(id=id)
        except StageResult.DoesNotExist:
            raise StageResultNotFoundException(id)
