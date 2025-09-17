import abc
from typing import List

from src.modules.profile.domain.profile.aggregate import Profile
from src.modules.profile.domain.profile.value_objects.sex import Sex
from src.modules.user.domain.types import TUserId


class IProfileRepository:

    @abc.abstractmethod
    def add(self, profile: Profile) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def save(self, profile: Profile) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, profile: Profile) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_by_user_id(self, user_id: TUserId) -> Profile:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_next_profile(
        self,
        rank: int,
        user_id: int,
        ages: List[int],
        city: str,
        sex: Sex,
        interest: Sex | None = None,
        skip_current: bool = True,
    ) -> Profile | None:
        raise NotImplementedError
