from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class KronoliveInscriptionRow:
    dorsal: str
    team_name: str
    driver_name: str
    codriver_name: Optional[str]
    car_brand: str
    car_model: str
    car_group: str
    category: str
