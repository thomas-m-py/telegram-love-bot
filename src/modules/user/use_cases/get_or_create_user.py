from dataclasses import dataclass

from stories import Story, I, State, Variable, Argument

from src.modules.user.domain.user.aggregate import User
from src.modules.user.domain.user.repository import IUserRepository
from src.modules.user.use_cases.dto import CreateUserDTO


class GetOrCreateUserState(State):
    user_data: CreateUserDTO = Argument()

    user: User = Variable()


@dataclass
class GetOrCreateUserCase(Story):

    I.find_user
    I.create_if_not_exists
    I.save

    async def find_user(self, state: GetOrCreateUserState):
        state.user = await self.user_repository.find_by_tid(state.user_data.tid)

    async def create_if_not_exists(self, state: GetOrCreateUserState):
        if state.user:
            return

        new_user = User.create(
            user_id=state.user_data.tid,
            first_name=state.user_data.first_name,
            last_name=state.user_data.last_name,
            username=state.user_data.username,
            language=state.user_data.language,
        )
        state.user = new_user

    async def save(self, state: GetOrCreateUserState):
        self.user_repository.add(state.user)
        await self.user_repository.save(state.user)

    user_repository: IUserRepository
