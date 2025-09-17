from dataclasses import dataclass

from stories import Story, I, State, Variable, Argument

from src.modules.user.domain.user.aggregate import User
from src.modules.user.domain.user.errors import UserNotFoundError
from src.modules.user.domain.user.repository import IUserRepository
from src.modules.user.use_cases.dto import UpdateUserDTO


class UpdateUserState(State):
    update: UpdateUserDTO = Argument()

    user: User = Variable()


@dataclass
class UpdateUserCase(Story):

    I.find_user
    I.update_user
    I.save

    async def find_user(self, state: UpdateUserState):
        user = await self.user_repository.find_by_tid(state.update.tid)
        if user is None:
            raise UserNotFoundError
        state.user = user

    async def update_user(self, state: UpdateUserState):
        user = state.user
        update = state.update

        if update.first_name:
            user.set_first_name(update.first_name)

        if update.last_name:
            user.set_last_name(update.last_name)

        if update.username:
            user.set_username(update.username)

        if update.language:
            user.set_lang(update.language)

    async def save(self, state: UpdateUserState):
        await self.user_repository.save(state.user)

    user_repository: IUserRepository
