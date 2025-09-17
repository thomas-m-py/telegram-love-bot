from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from src.bot.utils.keyboard import build_reply_keyboard
from src.bot.states.create_profile import CreateProfileForm

router = Router()


def parse_sex_from_choice(choice_text: str, i18n: I18nContext) -> int | None:
    if choice_text == i18n.i_am_men():
        return 0
    elif choice_text == i18n.i_am_woman():
        return 1


@router.message(F.text, CreateProfileForm.sex)
async def handle_sex_selection(message: Message, i18n: I18nContext, state: FSMContext):
    selected_sex = parse_sex_from_choice(message.text, i18n)

    if selected_sex is None:
        await message.answer(i18n.choice_your_sex())
        return

    await state.update_data(sex=selected_sex)
    await state.set_state(CreateProfileForm.interest)

    await message.answer(
        i18n.choice_interest(),
        reply_markup=build_reply_keyboard(
            i18n.interest_men(),
            i18n.interest_woman(),
            i18n.interest_doesnt_matter(),
        ),
    )
