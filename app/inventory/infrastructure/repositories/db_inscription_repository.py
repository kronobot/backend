from uuid import UUID

from inventory.domain.inscription import Inscription
from inventory.domain.exceptions.inscription_not_found_exception import InscriptionNotFoundException
from inventory.domain.repositories.inscription_criteria import InscriptionCriteria
from inventory.domain.repositories.inscription_repository import InscriptionRepository


class DbInscriptionRepository(InscriptionRepository):
    def save(self, inscription: Inscription) -> None:
        inscription.save()

    def find_by_criteria(self, criteria: InscriptionCriteria) -> list[Inscription]:
        queryset = Inscription.objects.select_related("team", "driver", "codriver", "car")

        if criteria.id is not None:
            queryset = queryset.filter(id=criteria.id)
        if criteria.event is not None:
            queryset = queryset.filter(event_id=criteria.event)
        if criteria.category is not None:
            queryset = queryset.filter(category=criteria.category)
        if criteria.team is not None:
            queryset = queryset.filter(team_id=criteria.team)
        if criteria.driver is not None:
            queryset = queryset.filter(driver_id=criteria.driver)
        if criteria.codriver is not None:
            queryset = queryset.filter(codriver_id=criteria.codriver)
        if criteria.car is not None:
            queryset = queryset.filter(car_id=criteria.car)
        if criteria.dorsal is not None:
            queryset = queryset.filter(dorsal=criteria.dorsal)
        if criteria.total_seconds is not None:
            queryset = queryset.filter(total_seconds=criteria.total_seconds)
        if criteria.total_rank is not None:
            queryset = queryset.filter(total_rank=criteria.total_rank)
        if criteria.total_penalty_seconds is not None:
            queryset = queryset.filter(total_penalty_seconds=criteria.total_penalty_seconds)

        return list(queryset)

    def find_or_fail_by_id(self, id: UUID) -> Inscription:
        try:
            return Inscription.objects.get(id=id)
        except Inscription.DoesNotExist:
            raise InscriptionNotFoundException(id)
