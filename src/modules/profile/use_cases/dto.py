from dataclasses import dataclass
from typing import List

from src.modules.profile.domain.profile.value_objects.age import Age
from src.modules.profile.domain.profile.value_objects.city import City
from src.modules.profile.domain.profile.value_objects.bio import Bio
from src.modules.profile.domain.profile.value_objects.media import Media
from src.modules.profile.domain.profile.value_objects.name import Name
from src.modules.profile.domain.profile.value_objects.sex import Sex
from src.modules.user.domain.types import TUserId


@dataclass
class ProfileInfoDTO:

    user_id: TUserId
    name: Name
    age: Age
    city: City
    sex: Sex
    media: List[Media]
    bio: Bio | None = None
    interest: Sex | None = None


@dataclass
class UpdateMediaDTO:
    media: List[Media]
    clear: bool


@dataclass
class UpdateProfileDTO:
    name: Name | None = None
    age: Age | None = None
    city: City | None = None
    sex: Sex | None = None
    bio: Bio | None = None
    interest: Sex | None = None
    media: UpdateMediaDTO | None = None
