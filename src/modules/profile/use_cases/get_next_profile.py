from dataclasses import dataclass
from typing import List

from stories import Story, I, State, Variable, Argument

from src.modules.profile.domain.profile.aggregate import Profile
from src.modules.profile.domain.profile.errors import ProfileNotFoundError
from src.modules.profile.domain.profile.repository import IProfileRepository
from src.modules.user.domain.types import TUserId
from src.settings.const import FIND_AGE_RANGE


def get_ages_range(age: int, range_: int = FIND_AGE_RANGE) -> List[int]:
    min_age = age - range_
    max_age = age + range_
    if min_age < 18 <= age:
        min_age = 18

    return list(range(min_age, max_age + 1))


async def _get_next_profile(
    repository: IProfileRepository, for_profile: Profile, skip_current: bool
) -> Profile | None:
    return await repository.get_next_profile(
        for_profile.rank_cursor,
        for_profile.profile_cursor,
        ages=get_ages_range(int(for_profile.age)),
        city=str(for_profile.city),
        sex=for_profile.sex,
        interest=for_profile.interest,
        skip_current=skip_current,
    )


class ResolveProfileState(State):
    user_id: TUserId = Argument()
    skip_current: bool = Argument()

    profile: Profile = Variable()
    next_profile: Profile = Variable()


@dataclass
class ResolveProfile(Story):

    I.find_profile
    I.get_next_profile
    I.save

    async def find_profile(self, state: ResolveProfileState):
        profile = await self.profile_repository.find_by_user_id(state.user_id)
        if profile is None:
            raise ProfileNotFoundError
        state.profile = profile

    async def get_next_profile(self, state: ResolveProfileState):
        next_profile = await _get_next_profile(
            self.profile_repository, state.profile, state.skip_current
        )

        if (
            next_profile is None
            and state.profile.rank_cursor is not None
            and state.profile.profile_cursor is not None
        ):
            state.profile.set_profile_cursor(None)
            state.profile.set_rank_cursor(None)
            next_profile = await _get_next_profile(
                self.profile_repository, state.profile, True
            )

        if not state.skip_current:
            state.next_profile = next_profile
            return

        if next_profile:
            state.profile.set_profile_cursor(next_profile.user_id)
            state.profile.set_rank_cursor(int(next_profile.rank))

        state.next_profile = next_profile

    async def save(self, state: ResolveProfileState):
        await self.profile_repository.save(state.profile)

    profile_repository: IProfileRepository
