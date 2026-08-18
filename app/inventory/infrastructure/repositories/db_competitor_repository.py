from uuid import UUID

from inventory.domain.competitor import Competitor
from inventory.domain.exceptions.competitor_not_found_exception import CompetitorNotFoundException
from inventory.domain.repositories.competitor_criteria import CompetitorCriteria
from inventory.domain.repositories.competitor_repository import CompetitorRepository


class DbCompetitorRepository(CompetitorRepository):
    def save(self, competitor: Competitor) -> None:
        competitor.save()

    def find_by_criteria(self, criteria: CompetitorCriteria) -> list[Competitor]:
        queryset = Competitor.objects.all()

        if criteria.id is not None:
            queryset = queryset.filter(id=criteria.id)
        if criteria.name is not None:
            queryset = queryset.filter(name=criteria.name)
        if criteria.name_normalized is not None:
            queryset = queryset.filter(name_normalized=criteria.name_normalized)
        if criteria.team is not None:
            queryset = queryset.filter(team_id=criteria.team)

        return list(queryset)

    def find_or_fail_by_id(self, id: UUID) -> Competitor:
        try:
            return Competitor.objects.get(id=id)
        except Competitor.DoesNotExist:
            raise CompetitorNotFoundException(id)

    def delete(self, competitor: Competitor) -> None:
        competitor.delete()
