from dataclasses import dataclass

from stories import Story, I, State, Variable, Argument

from src.modules.profile.domain.profile.aggregate import Profile
from src.modules.profile.domain.profile.repository import IProfileRepository
from src.modules.profile.use_cases.dto import ProfileInfoDTO


class CreateProfileState(State):
    profile_info: ProfileInfoDTO = Argument()

    profile: Profile = Variable()


@dataclass
class CreateProfile(Story):

    I.create_profile
    I.save

    async def create_profile(self, state: CreateProfileState):
        new_profile = Profile.create(
            user_id=state.profile_info.user_id,
            name=state.profile_info.name,
            age=state.profile_info.age,
            city=state.profile_info.city,
            sex=state.profile_info.sex,
            bio=state.profile_info.bio,
            media=state.profile_info.media,
            interest=state.profile_info.interest,
        )
        state.profile = new_profile

    async def save(self, state: CreateProfileState):
        self.profile_repository.add(state.profile)
        await self.profile_repository.save(state.profile)

    profile_repository: IProfileRepository
