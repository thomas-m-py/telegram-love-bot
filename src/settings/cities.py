import os
from pathlib import Path

CITIES_DIR = Path(__file__).parent.parent.parent.absolute() / "cities"


def load_data():
    cities = set()
    aliases = {}
    for file_name in os.listdir(CITIES_DIR):
        if not file_name.endswith(".txt"):
            continue

        path = os.path.join(CITIES_DIR, file_name)

        if file_name.endswith("_aliases.txt"):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    if not line:
                        continue
                    if ":" not in line:
                        continue

                    full, line_aliases = line.split(":", 1)
                    full = full.strip()
                    for alias in line_aliases.split(","):
                        aliases[alias.strip()] = full
            continue
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    cities.add(line)

    return cities, aliases


CITIES = load_data()
