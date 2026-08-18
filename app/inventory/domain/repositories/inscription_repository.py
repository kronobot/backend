from abc import ABC, abstractmethod
from uuid import UUID

from inventory.domain.inscription import Inscription
from inventory.domain.repositories.inscription_criteria import InscriptionCriteria


class InscriptionRepository(ABC):
    @abstractmethod
    def save(self, inscription: Inscription) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_criteria(self, criteria: InscriptionCriteria) -> list[Inscription]:
        raise NotImplementedError

    @abstractmethod
    def find_or_fail_by_id(self, id: UUID) -> Inscription:
        raise NotImplementedError
