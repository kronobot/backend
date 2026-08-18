import re
import unicodedata


def normalize_name(name: str) -> str:
    collapsed = re.sub(r"\s+", " ", name.strip())
    folded = unicodedata.normalize("NFKD", collapsed).encode("ascii", "ignore").decode()
    return folded.casefold()
