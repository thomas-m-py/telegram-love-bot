from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext, LazyProxy
from dishka import FromDishka

from src.bot.handlers.helpers.find_profile import find_profile
from src.bot.states.create_profile import CreateProfileForm
from src.modules.profile.domain.profile.value_objects.media import Media, MediaType
from src.modules.profile.domain.profile.value_objects.sex import Sex
from src.modules.profile.infra.db.profile_repository import ProfileRepository
from src.modules.profile.use_cases.create_profile import (
    CreateProfileState,
    CreateProfile,
)
from src.modules.profile.use_cases.edit_profile import EditProfileState, EditProfile
from src.modules.profile.use_cases.dto import (
    ProfileInfoDTO,
    UpdateProfileDTO,
    UpdateMediaDTO,
)
from src.modules.profile.domain.profile.value_objects.age import Age
from src.modules.profile.domain.profile.value_objects.city import City
from src.modules.profile.domain.profile.value_objects.bio import Bio
from src.modules.profile.domain.profile.value_objects.name import Name
from src.modules.user.domain.types import TUserId

router = Router()


def convert_sex_int_to_enum(sex: int) -> Sex | None:
    if sex == 0:
        return Sex.MALE
    elif sex == 1:
        return Sex.FEMALE
    return None


@router.message(F.text == LazyProxy("agree_profile"), CreateProfileForm.confirm)
async def handle_profile_confirmation(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
):
    state_data = await state.get_data()

    profile_data = _build_profile_data_from_state(state_data, message.from_user.id)
    is_creating_new = state_data.get("is_create", True)

    if is_creating_new:
        await _create_new_profile(profile_data, profile_repository)
    else:
        await _update_existing_profile(
            profile_data, profile_repository, message.from_user.id
        )

    await state.clear()
    await find_profile(
        message=message, i18n=i18n, state=state, profile_repository=profile_repository
    )


def create_media_objects_from_raw(raw_media_list: list[tuple[str, str]]) -> list[Media]:
    media_objects = []
    for file_id, media_type_str in raw_media_list:
        media_objects.append(
            Media.create(file_id=file_id, media_type=MediaType(media_type_str.upper()))
        )
    return media_objects


def _build_profile_data_from_state(state_data: dict, user_id: int) -> dict:
    sex = convert_sex_int_to_enum(state_data.get("sex"))
    interest = convert_sex_int_to_enum(state_data.get("interest"))
    bio_text = state_data.get("bio")
    raw_media = state_data.get("media", [])

    return {
        "user_id": TUserId(user_id),
        "name": Name.create(state_data.get("name")),
        "age": Age.create(state_data.get("age")),
        "city": City.create(state_data.get("city")),
        "sex": sex,
        "interest": interest,
        "bio": Bio.create(bio_text) if bio_text else None,
        "media": create_media_objects_from_raw(raw_media),
    }


async def _create_new_profile(profile_data: dict, repository: ProfileRepository):
    profile_info = ProfileInfoDTO(
        user_id=profile_data["user_id"],
        name=profile_data["name"],
        age=profile_data["age"],
        city=profile_data["city"],
        sex=profile_data["sex"],
        bio=profile_data["bio"],
        media=profile_data["media"],
        interest=profile_data["interest"],
    )

    create_state = CreateProfileState(profile_info=profile_info)
    create_profile_use_case = CreateProfile(profile_repository=repository)
    await create_profile_use_case(create_state)


async def _update_existing_profile(
    profile_data: dict, repository: ProfileRepository, user_id: int
):
    update_info = UpdateProfileDTO(
        name=profile_data["name"],
        age=profile_data["age"],
        city=profile_data["city"],
        sex=profile_data["sex"],
        bio=profile_data["bio"],
        interest=profile_data["interest"],
        media=UpdateMediaDTO(media=profile_data["media"], clear=True),
    )

    edit_state = EditProfileState(
        user_id=TUserId(user_id),
        update_profile_info=update_info,
    )

    edit_profile_use_case = EditProfile(profile_repository=repository)
    await edit_profile_use_case(edit_state)
