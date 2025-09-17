import difflib

from src.settings.cities import CITIES


def find_similar(query: str, cities: set) -> str | None:
    query_lower = query.lower()
    matches = difflib.get_close_matches(
        query_lower, [c.lower() for c in cities], n=1, cutoff=0.6
    )
    if matches:
        for city in cities:
            if city.lower() == matches[0]:
                return city
    return None


def find_city(query: str) -> [str | None, bool]:
    cities, aliases = CITIES
    query = query.strip()

    for city in cities:
        if city.lower() == query.lower():
            return city, True

    alias_full = aliases.get(query.lower())
    if alias_full and alias_full in cities:
        return alias_full, True

    return find_similar(query, cities), False
