from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import LazyProxy, I18nContext
from dishka import FromDishka

from src.bot.handlers.helpers.find_profile import find_profile
from src.bot.states.editing_profile import MyProfileForm
from src.bot.utils.keyboard import build_reply_keyboard
from src.modules.profile.domain.profile.errors import BioTooShortError, BioTooLongError
from src.modules.profile.domain.profile.value_objects.bio import Bio
from src.modules.profile.domain.profile.value_objects.media import Media, MediaType
from src.modules.profile.use_cases.dto import UpdateProfileDTO, UpdateMediaDTO
from src.modules.profile.use_cases.edit_profile import EditProfileState, EditProfile
from src.bot.handlers.helpers.show_profile import build_profile
from src.modules.profile.infra.db.profile_repository import ProfileRepository
from src.modules.user.domain.types import TUserId
from src.settings.const import MAX_NUM_MEDIA

router = Router()


async def show_profile_menu(message: Message, i18n: I18nContext):
    profile_menu_keyboard = build_reply_keyboard(
        i18n.profile_menu_look_profiles_button_text(),
        i18n.profile_menu_edit_profile_button_text(),
        i18n.profile_menu_edit_profile_media_button_text(),
        i18n.profile_menu_edit_profile_bio_button_text(),
    )
    await message.answer(
        i18n.profile_menu(),
        reply_markup=profile_menu_keyboard,
    )


async def show_my_profile(
    message: Message,
    i18n: I18nContext,
    repository: ProfileRepository,
):
    profile = await repository.find_by_user_id(TUserId(message.from_user.id))
    if not profile:
        await message.answer(i18n.your_profile_not_created())
        return

    await message.answer(i18n.your_profile_look())
    await message.answer_media_group(build_profile(profile).build())
    await show_profile_menu(
        message=message,
        i18n=i18n,
    )


@router.message(
    F.text.in_([LazyProxy("menu_my_profile_button_text")]),
    StateFilter(None),
)
async def my_profile(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
) -> None:
    await show_my_profile(message=message, i18n=i18n, repository=profile_repository)
    await state.set_state(MyProfileForm.view)


@router.message(
    F.text == LazyProxy("profile_menu_look_profiles_button_text"), MyProfileForm.view
)
async def find_profiles(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
) -> None:
    await state.clear()
    await find_profile(
        message=message, i18n=i18n, state=state, profile_repository=profile_repository
    )


@router.message(
    F.text == LazyProxy("profile_menu_edit_profile_media_button_text"),
    MyProfileForm.view,
)
async def update_media_profile(
    message: Message, i18n: I18nContext, state: FSMContext
) -> None:
    await message.answer(
        i18n.update_media_text(),
        reply_markup=build_reply_keyboard(i18n.go_back()),
    )
    await state.set_state(MyProfileForm.edit_media)


@router.message(F.text == LazyProxy("go_back"), MyProfileForm.edit_media)
async def update_media_profile(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
) -> None:
    await show_my_profile(message=message, i18n=i18n, repository=profile_repository)
    await state.update_data(media=[])
    await state.set_state(MyProfileForm.view)


@router.message(F.content_type.in_({"video", "photo"}), MyProfileForm.edit_media)
async def upload_photo(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
) -> None:
    if message.video:
        file_id = message.video.file_id
        media_type = "video"
    elif message.photo:
        file_id = message.photo[-1].file_id
        media_type = "photo"
    else:
        return

    data = await state.get_data()
    media = data.get("media", [])
    media.append((file_id, media_type))

    await state.update_data(media=media)

    remaining_slots = MAX_NUM_MEDIA - len(media)
    await message.answer(
        i18n.media_uploaded(media_count_can_add=remaining_slots),
        reply_markup=build_reply_keyboard(i18n.go_back(), i18n.thats_all_save()),
    )


@router.message(F.text == LazyProxy("thats_all_save"), MyProfileForm.edit_media)
async def save_media(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
) -> None:

    data = await state.get_data()
    raw_media = data.get("media", [])

    if len(raw_media) == 0:
        await show_my_profile(message=message, i18n=i18n, repository=profile_repository)
        await state.set_state(MyProfileForm.view)
        return

    media = []
    for raw in raw_media:
        file_id = raw[0]
        file_type = raw[1]
        media.append(
            Media.create(file_id=file_id, media_type=MediaType(file_type.upper()))
        )

    state_ = EditProfileState(
        user_id=TUserId(message.from_user.id),
        update_profile_info=UpdateProfileDTO(
            media=UpdateMediaDTO(media=media, clear=True)
        ),
    )
    edit = EditProfile(profile_repository=profile_repository)
    await edit(state_)

    await state.update_data(media=[])
    await state.set_state(MyProfileForm.view)
    await show_my_profile(message=message, i18n=i18n, repository=profile_repository)


@router.message(
    F.text == LazyProxy("profile_menu_edit_profile_bio_button_text"), MyProfileForm.view
)
async def update_bio_profile(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
) -> None:
    await message.answer(
        i18n.update_bio_text(),
        reply_markup=build_reply_keyboard(i18n.go_back()),
    )
    await state.set_state(MyProfileForm.edit_bio)


@router.message(F.text == LazyProxy("go_back"), MyProfileForm.edit_bio)
async def update_bio_profile_back(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
) -> None:
    await state.set_state(MyProfileForm.view)
    await show_my_profile(message=message, i18n=i18n, repository=profile_repository)


@router.message(F.text, MyProfileForm.edit_bio)
async def update_bio_profile(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
) -> None:

    text = message.text
    try:
        state_ = EditProfileState(
            user_id=TUserId(message.from_user.id),
            update_profile_info=UpdateProfileDTO(bio=Bio.create(text)),
        )
        edit = EditProfile(profile_repository=profile_repository)
        await edit(state_)
    except BioTooShortError:
        await message.answer(i18n.bio_short())
        return
    except BioTooLongError:
        await message.answer(i18n.bio_long())
        return

    await state.set_state(MyProfileForm.view)
    await show_my_profile(message=message, i18n=i18n, repository=profile_repository)
