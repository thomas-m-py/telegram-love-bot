from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_i18n import LazyFilter, I18nContext, LazyProxy
from dishka import FromDishka

from src.bot.utils.keyboard import build_reply_keyboard
from src.bot.handlers.my_profile import show_my_profile
from src.bot.states.create_profile import CreateProfileForm
from src.bot.states.editing_profile import MyProfileForm
from src.modules.profile.infra.db.profile_repository import ProfileRepository

router = Router()


@router.message(LazyFilter("lets_go"))
async def handle_start_profile_creation(
    message: Message, i18n: I18nContext, state: FSMContext
) -> None:
    await message.answer(i18n.enter_your_age(), reply_markup=ReplyKeyboardRemove())
    await state.set_state(CreateProfileForm.age)


@router.message(
    F.text == LazyProxy("profile_menu_edit_profile_button_text"), MyProfileForm.view
)
async def handle_edit_profile_start(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
) -> None:
    profile = await profile_repository.find_by_user_id(user_id=message.from_user.id)

    keyboard = ReplyKeyboardRemove()

    if profile:
        media_list = []
        for media_item in profile.media:
            media_list.append((media_item.file_id, media_item.media_type.value.lower()))
        existing_data = {
            "name": str(profile.name),
            "age": int(profile.age),
            "city": str(profile.city),
            "bio": str(profile.bio) if profile.bio else None,
            "prev_media": media_list,
            "is_create": False,
        }
        await state.update_data(**existing_data)
        keyboard = build_reply_keyboard(str(int(profile.age)))

    await state.set_state(CreateProfileForm.age)
    await message.answer(i18n.enter_your_age(), reply_markup=keyboard)


@router.message(F.text == LazyProxy("edit_profile"), CreateProfileForm.confirm)
async def handle_profile_edit_restart(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
):
    state_data = await state.get_data()

    if not state_data.get("is_create", True):
        await show_my_profile(message=message, i18n=i18n, repository=profile_repository)
        await state.set_state(MyProfileForm.view)
        return

    previous_age = state_data.get("age")
    keyboard = ReplyKeyboardRemove()
    if previous_age:
        keyboard = build_reply_keyboard(str(previous_age))

    await state.set_state(CreateProfileForm.age)
    await message.answer(i18n.enter_your_age(), reply_markup=keyboard)
