from typing import List

from src.modules.profile.domain.profile.errors import MediaLimitExceededError
from src.settings.const import MAX_NUM_MEDIA, DEFAULT_RANK

from src.common.domain.aggregate import RootEntity
from src.modules.profile.domain.profile.value_objects.age import Age
from src.modules.profile.domain.profile.value_objects.city import City
from src.modules.profile.domain.profile.value_objects.bio import Bio
from src.modules.profile.domain.profile.value_objects.media import Media
from src.modules.profile.domain.profile.value_objects.name import Name
from src.modules.profile.domain.profile.value_objects.rank import Rank
from src.modules.profile.domain.profile.value_objects.sex import Sex
from src.modules.user.domain.types import TUserId


class Profile(RootEntity):

    def __init__(
        self,
        user_id: TUserId,
        rank: Rank,
        name: Name,
        age: Age,
        city: City,
        sex: Sex,
        media: List[Media],
        is_active: bool,
        bio: Bio | None = None,
        interest: Sex | None = None,
        profile_cursor: int | None = None,
        rank_cursor: int | None = None,
    ):
        self._domain_events = []

        self._user_id = user_id
        self._rank = rank
        self._name = name
        self._age = age
        self._city = city
        self._sex = sex
        self._bio = bio
        self._media = media
        self._is_active = is_active
        self._interest = interest
        self._profile_cursor = profile_cursor
        self._rank_cursor = rank_cursor

    @property
    def user_id(self) -> TUserId:
        return self._user_id

    @property
    def rank(self) -> Rank:
        return self._rank

    @property
    def name(self) -> Name:
        return self._name

    @property
    def age(self) -> Age:
        return self._age

    @property
    def city(self) -> City:
        return self._city

    @property
    def bio(self) -> Bio | None:
        return self._bio

    @property
    def sex(self) -> Sex:
        return self._sex

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def media(self) -> List[Media]:
        return self._media

    @property
    def interest(self) -> Sex | None:
        return self._interest

    @property
    def profile_cursor(self) -> int | None:
        return self._profile_cursor

    @property
    def rank_cursor(self) -> int | None:
        return self._rank_cursor

    @classmethod
    def create(
        cls,
        user_id: TUserId,
        name: Name,
        age: Age,
        city: City,
        sex: Sex,
        media: List[Media],
        bio: Bio | None = None,
        interest: Sex | None = None,
    ) -> "Profile":

        if len(media) > MAX_NUM_MEDIA:
            raise MediaLimitExceededError

        new_profile = cls(
            user_id=user_id,
            rank=Rank.create(DEFAULT_RANK),
            name=name,
            age=age,
            city=city,
            sex=sex,
            bio=bio,
            media=media,
            interest=interest,
            is_active=True,
        )

        return new_profile

    def set_profile_cursor(self, cursor: int | None) -> None:
        self._profile_cursor = cursor

    def set_rank_cursor(self, cursor: int | None) -> None:
        self._rank_cursor = cursor

    def add_media(self, media: Media) -> None:
        if len(self._media) >= MAX_NUM_MEDIA:
            raise MediaLimitExceededError

        self._media.append(media)

    def set_name(self, name: Name) -> None:
        self._name = name

    def set_age(self, age: Age) -> None:
        self._age = age

    def set_city(self, city: City) -> None:
        self._city = city

    def set_sex(self, sex: Sex) -> None:
        self._sex = sex

    def set_bio(self, bio: Bio) -> None:
        self._bio = bio

    def set_interest(self, interest: Sex) -> None:
        self._interest = interest

    def clear_media(self) -> None:
        self._media.clear()

    def activate(self) -> None:
        self._is_active = True

    def deactivate(self) -> None:
        self._is_active = False
