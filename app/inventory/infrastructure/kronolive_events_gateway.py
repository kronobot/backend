import os
import re
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from django.conf import settings

from inventory.domain.event import Event
from inventory.domain.event_categories import EventCategories
from inventory.domain.event_providers import EventProviders
from inventory.domain.event_stage_status import EventStageStatus
from inventory.domain.inscription_category import InscriptionCategory
from inventory.infrastructure.kronolive_inscription_row import KronoliveInscriptionRow
from inventory.infrastructure.kronolive_stage_row import KronoliveStageRow
from inventory.infrastructure.kronolive_time_row import KronoliveStageValue, KronoliveTimeRow


class KronoliveEventsGateway:
    _CATEGORY_KEYWORDS = (
        ("rally", EventCategories.RALLY),
        ("pujada", EventCategories.HILL_CLIMB),
        ("kart", EventCategories.KARTING),
        ("autocros", EventCategories.AUTOCROSS),
    )

    _SECTION_CATEGORIES = {
        "REGULARITY SPORT": InscriptionCategory.REGULARITY_SPORT,
        "REGULARITY": InscriptionCategory.REGULARITY,
    }

    def get_events(self, year: int) -> list[Event]:
        response = requests.get(f"{settings.KRONOLIVE_BASE_URL}/en/{year}")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        events = []
        for card_body in soup.find_all("div", class_="card-body"):
            link = card_body.find("a", href=True)
            if link is None:
                continue

            small = link.find("small")
            date_text = small.get_text(strip=True) if small else ""
            event_date = datetime.strptime(date_text, "%d/%m/%Y").date()

            name = link.contents[0].strip()

            event_url = urljoin(settings.KRONOLIVE_BASE_URL, link["href"])
            base_url = event_url.rsplit("/", 1)[0]

            event = Event(
                name=name,
                start_date=event_date,
                end_date=event_date,
                category=self._detect_category(name),
                provider=EventProviders.KRONOLIVE,
                status=True,
                provider_event_url=event_url,
                provider_times_url=f"{base_url}/Tiempos",
                provider_inscriptions_url=f"{base_url}/ListaDeInscritos",
                provider_stages_url=f"{base_url}/TiemposOnline",
            )
            event.poster_url = self._extract_poster_url(card_body, settings.KRONOLIVE_BASE_URL)
            events.append(event)

        return events

    def _extract_poster_url(self, card_body, base_url: str) -> Optional[str]:
        style = card_body.get("style", "")
        match = re.search(r"background-image:\s*url\(['\"]?([^'\")]+)['\"]?\)", style)
        if match is None:
            return None

        resolved_url = urljoin(base_url, match.group(1))
        return resolved_url if "poster" in resolved_url.lower() else None

    def download_poster(self, poster_url: str) -> tuple[str, bytes]:
        response = requests.get(poster_url)
        response.raise_for_status()
        filename = os.path.basename(urlparse(poster_url).path)
        return filename, response.content

    def _detect_category(self, name: str) -> str:
        lowered = name.lower()
        for keyword, category in self._CATEGORY_KEYWORDS:
            if keyword in lowered:
                return category
        return ""

    def get_inscriptions(self, provider_inscriptions_url: str) -> list[KronoliveInscriptionRow]:
        response = requests.get(provider_inscriptions_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        if table is None:
            return []

        rows = []
        current_section = None

        for tr in table.find_all("tr"):
            cells = tr.find_all("td")

            if not cells:
                continue

            if len(cells) == 1:
                section_text = cells[0].get_text(strip=True)
                current_section = self._SECTION_CATEGORIES.get(section_text, current_section)
                continue

            dorsal = cells[0].get_text(strip=True)
            team_name = cells[1].get_text(strip=True)
            driver_name, codriver_name, car_brand, car_model, car_group = self._parse_entry_cells(cells)

            if current_section is not None:
                category = current_section
            elif codriver_name is None:
                category = InscriptionCategory.SOLO
            else:
                category = InscriptionCategory.WITH_CODRIVER

            rows.append(
                KronoliveInscriptionRow(
                    dorsal=dorsal,
                    team_name=team_name,
                    driver_name=driver_name,
                    codriver_name=codriver_name,
                    car_brand=car_brand,
                    car_model=car_model,
                    car_group=car_group,
                    category=category,
                )
            )

        return rows

    def _parse_entry_cells(self, cells) -> tuple[str, Optional[str], str, str, str]:
        """Returns (driver_name, codriver_name, car_brand, car_model, car_group)."""
        driver_cell = cells[2]
        for hidden in driver_cell.select(".d-sm-none"):
            hidden.decompose()
        driver_name = driver_cell.get_text(strip=True)
        codriver_name = cells[3].get_text(strip=True) or None
        vehicle_cell = cells[4]
        img = vehicle_cell.find("img")
        car_brand = img.get("title", "").strip() if img else ""
        car_model = vehicle_cell.get_text(strip=True)
        car_group = cells[6].get_text(strip=True)
        return driver_name, codriver_name, car_brand, car_model, car_group

    def get_stages(self, provider_stages_url: str) -> list[KronoliveStageRow]:
        response = requests.get(provider_stages_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="tablatiempos")
        if table is None:
            return []

        rows = []
        for tr in table.find_all("tr"):
            cells = tr.find_all("td")
            if len(cells) < 7:
                continue

            code = cells[0].get_text(strip=True)
            loop, loop_position = self._parse_stage_code(code)

            rows.append(
                KronoliveStageRow(
                    order=len(rows) + 1,
                    loop=loop,
                    loop_position=loop_position,
                    name=cells[1].get_text(strip=True),
                    date=datetime.strptime(cells[2].get_text(strip=True), "%d/%m/%Y").date(),
                    time=datetime.strptime(cells[3].get_text(strip=True), "%H:%M").time(),
                    distance_km=self._parse_distance_km(cells[4].get_text(strip=True)),
                    status=self._parse_stage_status(cells[5].get_text(strip=True)),
                    finished_count=int(cells[6].get_text(strip=True)),
                )
            )

        return rows

    def _parse_stage_code(self, code: str) -> tuple[str, int]:
        match = re.match(r"^([A-Za-z]+)(\d+)$", code)
        return match.group(1), int(match.group(2))

    def _parse_distance_km(self, text: str) -> float:
        return float(text.replace("km", "").strip().replace(".", "").replace(",", "."))

    def _parse_stage_status(self, text: str) -> str:
        mapping = {
            "pending": EventStageStatus.PENDING,
            "in progress": EventStageStatus.IN_PROGRESS,
            "finished": EventStageStatus.FINISHED,
        }
        return mapping[text.strip().lower()]

    def get_times(self, provider_times_url: str) -> list[KronoliveTimeRow]:
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                )
            }
        )
        initial = session.get(provider_times_url)
        initial.raise_for_status()
        soup = BeautifulSoup(initial.text, "html.parser")
        viewstate = soup.find("input", id="__VIEWSTATE")["value"]
        viewstate_generator = soup.find("input", id="__VIEWSTATEGENERATOR")["value"]
        event_validation = soup.find("input", id="__EVENTVALIDATION")["value"]

        rows_by_dorsal = {}
        for modality_value in self._get_modality_filter_values(soup):
            response = session.post(
                provider_times_url,
                data={
                    "ctl00$cphContenido$TopPrueba$ScriptManager1": (
                        "ctl00$cphContenido$UpdatePanel1|ctl00$cphContenido$DDFiltro"
                    ),
                    "__EVENTTARGET": "ctl00$cphContenido$DDFiltro",
                    "__EVENTARGUMENT": "",
                    "__LASTFOCUS": "",
                    "__VIEWSTATE": viewstate,
                    "__VIEWSTATEGENERATOR": viewstate_generator,
                    "__EVENTVALIDATION": event_validation,
                    "ctl00$cphContenido$DDFiltro": modality_value,
                    "__ASYNCPOST": "true",
                },
                headers={
                    "X-MicrosoftAjax": "Delta=true",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": provider_times_url,
                },
            )
            response.raise_for_status()
            html = self._extract_update_panel_html(response.text)
            for row in self._parse_times_table(html):
                rows_by_dorsal[row.dorsal] = row

        return list(rows_by_dorsal.values())

    def _get_modality_filter_values(self, soup: BeautifulSoup) -> list[str]:
        select = soup.find("select", id="ctl00_cphContenido_DDFiltro")
        values_by_label = {
            option.get_text(strip=True): option["value"] for option in select.find_all("option")
        }
        # Kronolive has used both spellings for the "Overall" modality across events/time
        # (seen live as "Overall classification" and, later, just "Overall") - accept either.
        label_variants = (
            ("Overall classification", "Overall"),
            ("Regularity Sport",),
            ("Regularity",),
        )
        values = []
        for variants in label_variants:
            for label in variants:
                if label in values_by_label:
                    values.append(values_by_label[label])
                    break
        return values

    def _extract_update_panel_html(self, text: str) -> str:
        marker = "|updatePanel|ctl00_cphContenido_UpdatePanel1|"
        marker_index = text.index(marker)
        length = int(text[:marker_index].rsplit("|", 1)[-1])
        content_start = marker_index + len(marker)
        return text[content_start : content_start + length]

    def _parse_times_table(self, html: str) -> list[KronoliveTimeRow]:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", class_="tablatiempos")
        if table is None:
            return []

        rows = []
        for tr in table.find_all("tr")[1:]:
            cells = tr.find_all("td")
            if not cells:
                continue

            dorsal = cells[0].get_text(strip=True)
            stage_cells = cells[2:-1]
            total_cell = cells[-1]

            stage_values = []
            for position, cell in enumerate(stage_cells, start=1):
                if not cell.get_text(strip=True):
                    continue
                value_text, rank, _ = self._extract_cell_value(cell)
                stage_values.append(
                    KronoliveStageValue(
                        stage_position=position,
                        value_seconds=self._parse_seconds(value_text),
                        rank=rank,
                    )
                )

            total_text, total_rank, total_penalty_seconds = self._extract_cell_value(total_cell)
            total_seconds = self._parse_seconds(total_text) if total_text else None

            rows.append(
                KronoliveTimeRow(
                    dorsal=dorsal,
                    stage_values=stage_values,
                    total_seconds=total_seconds,
                    total_rank=total_rank,
                    total_penalty_seconds=total_penalty_seconds,
                )
            )

        return rows

    def _extract_cell_value(self, cell) -> tuple[str, Optional[int], Optional[float]]:
        rank = None
        penalty_seconds = None

        for small in cell.find_all("small"):
            text = small.get_text(strip=True).strip("()")
            if "red" in small.get("style", "").lower():
                penalty_seconds = self._parse_seconds(text) if text else None
            else:
                digits = re.search(r"\d+", text)
                rank = int(digits.group()) if digits else None
            small.decompose()

        return cell.get_text(strip=True), rank, penalty_seconds

    def _parse_seconds(self, text: str) -> float:
        parts = text.split(":")
        return sum(float(part) * (60**index) for index, part in enumerate(reversed(parts)))
