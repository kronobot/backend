from uuid import UUID

from inventory.domain.car import Car
from inventory.domain.exceptions.car_not_found_exception import CarNotFoundException
from inventory.domain.repositories.car_criteria import CarCriteria
from inventory.domain.repositories.car_repository import CarRepository


class DbCarRepository(CarRepository):
    def save(self, car: Car) -> None:
        car.save()

    def find_by_criteria(self, criteria: CarCriteria) -> list[Car]:
        queryset = Car.objects.all()

        if criteria.id is not None:
            queryset = queryset.filter(id=criteria.id)
        if criteria.brand is not None:
            queryset = queryset.filter(brand=criteria.brand)
        if criteria.model is not None:
            queryset = queryset.filter(model=criteria.model)
        if criteria.group is not None:
            queryset = queryset.filter(group=criteria.group)
        if criteria.competitor is not None:
            queryset = queryset.filter(competitor_id=criteria.competitor)

        return list(queryset)

    def find_or_fail_by_id(self, id: UUID) -> Car:
        try:
            return Car.objects.get(id=id)
        except Car.DoesNotExist:
            raise CarNotFoundException(id)
