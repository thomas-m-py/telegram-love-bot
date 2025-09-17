from src.modules.user.domain.types import TUserId
from src.modules.user.domain.user.repository import IUserRepository


class UserTelegramIdUniqueness:
    def __init__(self, user_repository: IUserRepository):
        self.repo = user_repository

    async def is_unique(self, id_: TUserId) -> bool:
        return not (await self.repo.exists_by_tid(id_))
