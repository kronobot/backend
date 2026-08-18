from typing import Optional

from inventory.domain.car import Car
from inventory.domain.competitor import Competitor
from inventory.domain.event import Event
from inventory.domain.inscription import Inscription
from inventory.domain.normalize_name import normalize_name
from inventory.domain.repositories.car_criteria import CarCriteria
from inventory.domain.repositories.car_repository import CarRepository
from inventory.domain.repositories.competitor_criteria import CompetitorCriteria
from inventory.domain.repositories.competitor_repository import CompetitorRepository
from inventory.domain.repositories.event_repository import EventRepository
from inventory.domain.repositories.inscription_criteria import InscriptionCriteria
from inventory.domain.repositories.inscription_repository import InscriptionRepository
from inventory.domain.repositories.team_criteria import TeamCriteria
from inventory.domain.repositories.team_repository import TeamRepository
from inventory.domain.team import Team
from inventory.infrastructure.kronolive_events_gateway import KronoliveEventsGateway
from inventory.infrastructure.kronolive_inscription_row import KronoliveInscriptionRow
from notification.domain.notification_provider_name import NotificationProviderName
from notification.domain.notification_task import NotificationTask
from notification.domain.notification_task_name import NotificationTaskName
from notification.domain.repositories.notification_task_repository import NotificationTaskRepository

from inventory.application.import_inscriptions_kronolive.import_inscriptions_kronolive_command import (
    ImportInscriptionsKronoliveCommand,
)


class ImportInscriptionsKronoliveCommandHandler:
    def __init__(
        self,
        kronolive_gateway: KronoliveEventsGateway,
        event_repository: EventRepository,
        team_repository: TeamRepository,
        competitor_repository: CompetitorRepository,
        car_repository: CarRepository,
        inscription_repository: InscriptionRepository,
        notification_task_repository: NotificationTaskRepository,
    ):
        self.kronolive_gateway = kronolive_gateway
        self.event_repository = event_repository
        self.team_repository = team_repository
        self.competitor_repository = competitor_repository
        self.car_repository = car_repository
        self.inscription_repository = inscription_repository
        self.notification_task_repository = notification_task_repository

    def handle(self, command: ImportInscriptionsKronoliveCommand) -> int:
        event = self.event_repository.find_or_fail_by_id(command.event_id)
        rows = self.kronolive_gateway.get_inscriptions(event.provider_inscriptions_url)

        for row in rows:
            team = self._find_or_create_team(row.team_name)
            driver = self._find_or_create_competitor(row.driver_name, team)
            codriver = (
                self._find_or_create_competitor(row.codriver_name, team)
                if row.codriver_name is not None
                else None
            )
            car = self._find_or_create_car(row, driver)
            self._save_inscription(event, row, team, driver, codriver, car)

        return len(rows)

    def _find_or_create_team(self, name: str) -> Team:
        existing = self.team_repository.find_by_criteria(TeamCriteria(name_normalized=normalize_name(name)))
        if existing:
            return existing[0]

        team = Team(name=name, name_normalized=normalize_name(name))
        self.team_repository.save(team)
        return team

    def _find_or_create_competitor(self, name: str, team: Team) -> Competitor:
        existing = self.competitor_repository.find_by_criteria(
            CompetitorCriteria(name_normalized=normalize_name(name))
        )
        if existing:
            return existing[0]

        competitor = Competitor(name=name, name_normalized=normalize_name(name), team=team)
        self.competitor_repository.save(competitor)
        return competitor

    def _find_or_create_car(self, row: KronoliveInscriptionRow, driver: Competitor) -> Car:
        existing = self.car_repository.find_by_criteria(
            CarCriteria(
                brand=row.car_brand,
                model=row.car_model,
                group=row.car_group,
                competitor=driver.id,
            )
        )
        if existing:
            return existing[0]

        car = Car(brand=row.car_brand, model=row.car_model, group=row.car_group, competitor=driver)
        self.car_repository.save(car)
        return car

    def _save_inscription(
        self,
        event,
        row: KronoliveInscriptionRow,
        team: Team,
        driver: Competitor,
        codriver: Optional[Competitor],
        car: Car,
    ) -> None:
        existing = self.inscription_repository.find_by_criteria(
            InscriptionCriteria(event=event.id, dorsal=row.dorsal)
        )
        is_new = not existing

        if existing:
            inscription = existing[0]
            inscription.category = row.category
            inscription.team = team
            inscription.driver = driver
            inscription.codriver = codriver
            inscription.car = car
        else:
            inscription = Inscription(
                event=event,
                dorsal=row.dorsal,
                category=row.category,
                team=team,
                driver=driver,
                codriver=codriver,
                car=car,
            )

        self.inscription_repository.save(inscription)

        if is_new:
            self._notify_inscription_imported(event, inscription)

    def _notify_inscription_imported(self, event: Event, inscription: Inscription) -> None:
        notification_task = NotificationTask(
            event=event,
            provider=NotificationProviderName.DEBUG,
            name=NotificationTaskName.INSCRIPTIONS_IMPORTED,
            payload={"inscription_id": str(inscription.id), "dorsal": inscription.dorsal},
        )
        self.notification_task_repository.save(notification_task)
