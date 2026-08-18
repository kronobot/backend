from abc import ABC, abstractmethod
from uuid import UUID

from inventory.domain.car import Car
from inventory.domain.repositories.car_criteria import CarCriteria


class CarRepository(ABC):
    @abstractmethod
    def save(self, car: Car) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_criteria(self, criteria: CarCriteria) -> list[Car]:
        raise NotImplementedError

    @abstractmethod
    def find_or_fail_by_id(self, id: UUID) -> Car:
        raise NotImplementedError
