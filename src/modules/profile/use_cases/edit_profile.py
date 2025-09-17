from dataclasses import dataclass

from stories import Story, I, State, Variable, Argument

from src.modules.profile.domain.profile.errors import ProfileNotFoundError
from src.modules.user.domain.types import TUserId
from src.modules.profile.domain.profile.aggregate import Profile
from src.modules.profile.domain.profile.repository import IProfileRepository
from src.modules.profile.use_cases.dto import UpdateProfileDTO


class EditProfileState(State):
    user_id: TUserId = Argument()
    update_profile_info: UpdateProfileDTO = Argument()

    profile: Profile = Variable()


@dataclass
class EditProfile(Story):

    I.find_profile
    I.update_profile
    I.save

    async def find_profile(self, state: EditProfileState):
        profile = await self.profile_repository.find_by_user_id(state.user_id)
        if profile is None:
            raise ProfileNotFoundError

        state.profile = profile

    async def update_profile(self, state: EditProfileState):
        update = state.update_profile_info
        profile = state.profile
        if update.name:
            profile.set_name(update.name)

        if update.age:
            profile.set_age(update.age)

        if update.sex:
            profile.set_sex(update.sex)

        if update.interest:
            profile.set_interest(update.interest)

        if update.bio:
            profile.set_bio(update.bio)

        if update.city:
            profile.set_city(update.city)

        if update.media:
            if update.media.clear:
                profile.clear_media()
            for m in update.media.media:
                profile.add_media(m)

    async def save(self, state: EditProfileState):
        self.profile_repository.add(state.profile)
        await self.profile_repository.save(state.profile)

    profile_repository: IProfileRepository
