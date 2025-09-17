from dataclasses import dataclass

from stories import Story, I, State, Variable, Argument

from src.modules.user.domain.user.aggregate import User
from src.modules.user.domain.user.errors import UserAlreadyCreatedError
from src.modules.user.domain.user.repository import IUserRepository
from src.modules.user.domain.user.services import UserTelegramIdUniqueness
from src.modules.user.use_cases.dto import CreateUserDTO


class CreateUserState(State):
    user_data: CreateUserDTO = Argument()

    user: User = Variable()


@dataclass
class CreateUser(Story):

    I.check_tid_unique
    I.create_user
    I.save

    async def check_tid_unique(self, state: CreateUserState):
        is_unique = await UserTelegramIdUniqueness(self.user_repository).is_unique(
            state.user_data.tid
        )
        if not is_unique:
            raise UserAlreadyCreatedError

    async def create_user(self, state: CreateUserState):
        new_user = User.create(
            user_id=state.user_data.tid,
            first_name=state.user_data.first_name,
            last_name=state.user_data.last_name,
            username=state.user_data.username,
            language=state.user_data.language,
        )
        state.user = new_user

    async def save(self, state: CreateUserState):
        self.user_repository.add(state.user)
        await self.user_repository.save(state.user)

    user_repository: IUserRepository
