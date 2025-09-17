from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.user.infra.db.user_repository import UserRepository


class UserModuleProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.REQUEST)
    async def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session=session)
