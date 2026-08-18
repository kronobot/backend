from django.db import transaction

from inventory.domain.exceptions.cannot_merge_competitor_into_itself_exception import (
    CannotMergeCompetitorIntoItselfException,
)
from inventory.domain.repositories.car_criteria import CarCriteria
from inventory.domain.repositories.car_repository import CarRepository
from inventory.domain.repositories.competitor_repository import CompetitorRepository
from inventory.domain.repositories.inscription_criteria import InscriptionCriteria
from inventory.domain.repositories.inscription_repository import InscriptionRepository

from inventory.application.merge_competitors.merge_competitors_command import MergeCompetitorsCommand


class MergeCompetitorsCommandHandler:
    def __init__(
        self,
        competitor_repository: CompetitorRepository,
        inscription_repository: InscriptionRepository,
        car_repository: CarRepository,
    ):
        self.competitor_repository = competitor_repository
        self.inscription_repository = inscription_repository
        self.car_repository = car_repository

    def handle(self, command: MergeCompetitorsCommand) -> None:
        if command.winner_id == command.loser_id:
            raise CannotMergeCompetitorIntoItselfException(command.winner_id)

        with transaction.atomic():
            winner = self.competitor_repository.find_or_fail_by_id(command.winner_id)
            loser = self.competitor_repository.find_or_fail_by_id(command.loser_id)

            for inscription in self.inscription_repository.find_by_criteria(InscriptionCriteria(driver=loser.id)):
                inscription.driver = winner
                self.inscription_repository.save(inscription)

            for inscription in self.inscription_repository.find_by_criteria(InscriptionCriteria(codriver=loser.id)):
                inscription.codriver = winner
                self.inscription_repository.save(inscription)

            for car in self.car_repository.find_by_criteria(CarCriteria(competitor=loser.id)):
                car.competitor = winner
                self.car_repository.save(car)

            self.competitor_repository.delete(loser)
