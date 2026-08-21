from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup
import requests

from inventory.domain.inscription_category import InscriptionCategory
from inventory.infrastructure.kronolive_events_gateway import KronoliveEventsGateway
from inventory.infrastructure.kronolive_stage_row import KronoliveStageRow


class KronoliveHillclimbEventsGateway(KronoliveEventsGateway):
    _SECTION_CATEGORIES = {
        **KronoliveEventsGateway._SECTION_CATEGORIES,
        "SINGLE SPORT REGULARITY": InscriptionCategory.SINGLE_SPORT_REGULARITY,
        "DRIFT": InscriptionCategory.DRIFT,
    }

    _MODALITY_LABELS = (
        "General Montaña",
        "Special stage",
        "Regularity Sport",
        "Single Sport Regularity",
        "Regularity",
        "Drift",
    )

    def _parse_entry_cells(self, cells) -> tuple[str, Optional[str], str, str, str]:
        # Hillclimb pages have no dedicated co-driver column: the driver cell holds
        # "Driver<br>Codriver" (nested span) when there's a co-driver, or just "Driver"
        # otherwise. Vehicle/group columns are also shifted one index earlier than on
        # rally pages, since there's no separate co-driver <td>.
        driver_cell = cells[2]
        for hidden in driver_cell.select(".d-sm-none"):
            hidden.decompose()
        label = driver_cell.find("span", id=True) or driver_cell
        inner_span = label.find("span")
        if inner_span and inner_span.find("br"):
            codriver_name = inner_span.get_text(strip=True) or None
            inner_span.extract()
        else:
            codriver_name = None
        driver_name = label.get_text(strip=True)

        vehicle_cell = cells[3]
        img = vehicle_cell.find("img")
        car_brand = img.get("title", "").strip() if img else ""
        car_model = vehicle_cell.get_text(strip=True)
        car_group = cells[5].get_text(strip=True)
        return driver_name, codriver_name, car_brand, car_model, car_group

    def get_stages(self, provider_stages_url: str) -> list[KronoliveStageRow]:
        response = requests.get(provider_stages_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="tablatiempos")
        if table is None:
            return []

        rows = []
        heat_name = None

        for tr in table.find_all("tr"):
            cells = tr.find_all("td")

            if len(cells) == 1:
                heat_name = cells[0].get_text(strip=True)
                continue

            if len(cells) != 5 or heat_name is None:
                continue

            order = len(rows) + 1
            discipline_name = cells[0].get_text(strip=True)

            rows.append(
                KronoliveStageRow(
                    order=order,
                    loop="H",
                    loop_position=order,
                    name=f"{heat_name} - {discipline_name}",
                    date=datetime.strptime(cells[1].get_text(strip=True), "%d/%m/%Y").date(),
                    time=datetime.strptime(cells[2].get_text(strip=True), "%H:%M").time(),
                    distance_km=0.0,
                    status=self._parse_stage_status(cells[3].get_text(strip=True)),
                    finished_count=self._parse_finished_count(cells[4].get_text(strip=True)),
                )
            )

        return rows

    def _get_modality_filter_values(self, soup: BeautifulSoup) -> list[str]:
        select = soup.find("select", id="ctl00_cphContenido_DDFiltro")
        values_by_label = {
            option.get_text(strip=True): option["value"] for option in select.find_all("option")
        }
        return [values_by_label[label] for label in self._MODALITY_LABELS if label in values_by_label]
