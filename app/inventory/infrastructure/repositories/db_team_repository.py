from uuid import UUID

from inventory.domain.team import Team
from inventory.domain.exceptions.team_not_found_exception import TeamNotFoundException
from inventory.domain.repositories.team_criteria import TeamCriteria
from inventory.domain.repositories.team_repository import TeamRepository


class DbTeamRepository(TeamRepository):
    def save(self, team: Team) -> None:
        team.save()

    def find_by_criteria(self, criteria: TeamCriteria) -> list[Team]:
        queryset = Team.objects.all()

        if criteria.id is not None:
            queryset = queryset.filter(id=criteria.id)
        if criteria.name is not None:
            queryset = queryset.filter(name=criteria.name)
        if criteria.name_normalized is not None:
            queryset = queryset.filter(name_normalized=criteria.name_normalized)

        return list(queryset)

    def find_or_fail_by_id(self, id: UUID) -> Team:
        try:
            return Team.objects.get(id=id)
        except Team.DoesNotExist:
            raise TeamNotFoundException(id)
