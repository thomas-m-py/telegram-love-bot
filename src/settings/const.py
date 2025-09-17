import os
from pathlib import Path

import yaml

PROJECT_DIR = Path(__file__).resolve().parents[2]
CONFIG_FILE_PATH = os.path.join(PROJECT_DIR, "config.app.yaml")

with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
    application_config = yaml.safe_load(f)


# PROFILE SETTINGS
profile_config = application_config.get("Profile", {})

DEFAULT_RANK = profile_config.get("defaultRank", 100)
AGE_RESTRICTION = profile_config.get("ageRestriction", 14)
NOT_REAL_AGE = profile_config.get("notRealAge", 14)
FIND_AGE_RANGE = profile_config.get("findAgeRange", 2)
MIN_BIO_LEN = profile_config.get("minBioLength", 10)
MAX_BIO_LEN = profile_config.get("maxBioLength", 200)
MAX_NAME_LEN = profile_config.get("maxNameLength", 30)
MAX_NUM_MEDIA = profile_config.get("maxNumMedia", 3)

match_config = application_config.get("Match", {})

RECENT_MATCH_DAYS = match_config.get("recentMatchDays", 7)

LANGUAGES = application_config.get("Languages", {})
