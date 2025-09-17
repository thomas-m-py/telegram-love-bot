from dataclasses import dataclass

from stories import Story, I, State, Variable, Argument

from src.modules.profile.domain.profile.aggregate import Profile
from src.modules.profile.domain.profile.errors import ProfileNotFoundError
from src.modules.profile.domain.profile.repository import IProfileRepository
from src.modules.user.domain.types import TUserId


class ActivateProfileState(State):
    profile_id: TUserId = Argument()

    profile: Profile = Variable()


@dataclass
class ActivateProfileCase(Story):

    I.find_profile
    I.activate_profile
    I.save

    async def find_profile(self, state: ActivateProfileState):
        profile = await self.profile_repository.find_by_user_id(state.profile_id)
        if profile is None:
            raise ProfileNotFoundError
        state.profile = profile

    async def activate_profile(self, state: ActivateProfileState):
        state.profile.activate()

    async def save(self, state: ActivateProfileState):
        await self.profile_repository.save(state.profile)

    profile_repository: IProfileRepository
