from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.user.domain.types import TUserId
from src.modules.user.domain.user.aggregate import User
from src.modules.user.domain.user.repository import IUserRepository


class UserRepository(IUserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, user: User) -> None:
        self.session.add(user)

    async def save(self, user: User) -> None:
        await self.session.flush()
        await self.session.commit()

    async def delete(self, user: User) -> None:
        await self.session.delete(user)

    async def exists_by_tid(self, user_id: TUserId) -> bool:
        stmt = select(func.count()).where(User._id == user_id)
        result = await self.session.execute(stmt)
        return int(result.scalar_one()) > 0

    async def find_by_tid(self, tid: TUserId) -> User | None:
        return await self.session.get(User, tid)
