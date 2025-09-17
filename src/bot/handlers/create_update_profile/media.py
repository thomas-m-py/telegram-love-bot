from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, UserProfilePhotos, ReplyKeyboardRemove
from aiogram_i18n import I18nContext, LazyProxy

from src.bot.utils.keyboard import build_reply_keyboard
from src.bot.handlers.helpers.show_profile import build_profile
from src.bot.states.create_profile import CreateProfileForm
from src.settings.const import MAX_NUM_MEDIA

router = Router()


async def _show_profile_preview(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
):
    await state.set_state(CreateProfileForm.confirm)

    state_data = await state.get_data()
    profile_info = {
        "name": state_data.get("name", ""),
        "age": state_data.get("age", ""),
        "city": state_data.get("city", ""),
        "bio": state_data.get("bio", ""),
        "media": state_data.get("media", []),
    }

    profile_album = build_profile(profile_info)

    await message.answer(i18n.your_profile_look())
    await message.answer_media_group(profile_album.build())
    await message.answer(
        i18n.confirm_profile(),
        reply_markup=build_reply_keyboard(i18n.agree_profile(), i18n.edit_profile()),
    )


@router.message(F.text == LazyProxy("leave_previous"), CreateProfileForm.media)
async def handle_leave_previous_media(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
):
    state_data = await state.get_data()
    previous_media = state_data.get("prev_media")

    if previous_media is None:
        await message.answer(i18n.send_media())
        return

    await state.update_data(media=previous_media)
    await _show_profile_preview(message=message, i18n=i18n, state=state)


@router.message(F.text == LazyProxy("thats_all_save"), CreateProfileForm.media)
async def handle_media_save_completion(
    message: Message, i18n: I18nContext, state: FSMContext
):
    state_data = await state.get_data()
    media_list = state_data.get("media", [])

    if len(media_list) == 0:
        await message.answer(i18n.send_media())
        return

    await _show_profile_preview(message=message, i18n=i18n, state=state)


@router.message(
    F.text == LazyProxy("choice_from_telegram_account"), CreateProfileForm.media
)
async def handle_telegram_photo_selection(
    message: Message, i18n: I18nContext, state: FSMContext
):
    user_photos: UserProfilePhotos = await message.from_user.get_profile_photos()

    if user_photos.total_count == 0:
        await message.answer(i18n.no_media_account())
        await message.answer(i18n.send_media(), reply_markup=ReplyKeyboardRemove())
        return

    first_photo_file_id = user_photos.photos[0][-1].file_id
    media_list = [(first_photo_file_id, "photo")]

    await state.update_data(media=media_list)
    await _show_profile_preview(message=message, i18n=i18n, state=state)


@router.message(F.content_type.in_({"video", "photo"}), CreateProfileForm.media)
async def handle_media_upload(
    message: Message, i18n: I18nContext, state: FSMContext
) -> None:
    if message.video:
        file_id = message.video.file_id
        media_type = "video"
    elif message.photo:
        file_id = message.photo[-1].file_id
        media_type = "photo"
    else:
        await message.answer("??")
        return

    state_data = await state.get_data()
    current_media_list = state_data.get("media", [])

    if len(current_media_list) >= MAX_NUM_MEDIA:
        await _show_profile_preview(message=message, i18n=i18n, state=state)
        return

    current_media_list.append((file_id, media_type))
    await state.update_data(media=current_media_list)

    if len(current_media_list) >= MAX_NUM_MEDIA:
        await _show_profile_preview(message=message, i18n=i18n, state=state)
        return

    remaining_slots = MAX_NUM_MEDIA - len(current_media_list)
    await message.answer(
        i18n.media_uploaded(media_count_can_add=remaining_slots),
        reply_markup=build_reply_keyboard(i18n.thats_all_save()),
    )
