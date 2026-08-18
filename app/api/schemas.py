from datetime import date, time
from uuid import UUID

from ninja import Schema


class EventOut(Schema):
    id: UUID
    name: str
    start_date: date
    end_date: date
    category: str
    provider: str
    status: bool
    description: str


class EventStageOut(Schema):
    id: UUID
    order: int
    loop: str
    loop_position: int
    name: str
    date: date
    time: time
    distance_km: float
    status: str
    finished_count: int


class TeamOut(Schema):
    id: UUID
    name: str


class CompetitorOut(Schema):
    id: UUID
    name: str


class CarOut(Schema):
    id: UUID
    brand: str
    model: str
    group: str


class InscriptionOut(Schema):
    id: UUID
    category: str
    dorsal: str
    team: TeamOut
    driver: CompetitorOut
    codriver: CompetitorOut | None = None
    car: CarOut
    total_seconds: float | None = None
    total_rank: int | None = None
    total_penalty_seconds: float | None = None
