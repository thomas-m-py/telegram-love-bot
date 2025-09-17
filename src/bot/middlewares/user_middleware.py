from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from dishka import AsyncContainer

from src.modules.user.infra.db.user_repository import UserRepository
from src.modules.user.use_cases.dto import CreateUserDTO
from src.modules.user.use_cases.get_or_create_user import (
    GetOrCreateUserState,
    GetOrCreateUserCase,
)


class UserMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        di_container: AsyncContainer = data["dishka_container"]
        user_repository = await di_container.get(UserRepository)
        event_user: User = data["event_from_user"]

        state = GetOrCreateUserState(
            user_data=CreateUserDTO(
                tid=event_user.id,
                first_name=event_user.first_name,
                last_name=event_user.last_name,
                username=event_user.username,
                language=event_user.language_code,
            )
        )
        get_or_create_case = GetOrCreateUserCase(user_repository=user_repository)
        await get_or_create_case(state)
        data["user"] = state.user

        return await handler(event, data)
