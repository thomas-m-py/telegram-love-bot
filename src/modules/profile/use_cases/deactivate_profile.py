from dataclasses import dataclass

from stories import Story, I, State, Variable, Argument

from src.modules.profile.domain.profile.aggregate import Profile
from src.modules.profile.domain.profile.errors import ProfileNotFoundError
from src.modules.profile.domain.profile.repository import IProfileRepository
from src.modules.user.domain.types import TUserId


class DeactivateProfileState(State):
    profile_id: TUserId = Argument()

    profile: Profile = Variable()


@dataclass
class DeactivateProfileCase(Story):

    I.find_profile
    I.deactivate_profile
    I.save

    async def find_profile(self, state: DeactivateProfileState):
        profile = await self.profile_repository.find_by_user_id(state.profile_id)
        if profile is None:
            raise ProfileNotFoundError
        state.profile = profile

    async def deactivate_profile(self, state: DeactivateProfileState):
        state.profile.deactivate()

    async def save(self, state: DeactivateProfileState):
        await self.profile_repository.save(state.profile)

    profile_repository: IProfileRepository
