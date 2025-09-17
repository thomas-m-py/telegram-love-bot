from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.profile.infra.db.profile_repository import ProfileRepository


class ProfileModuleProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.REQUEST)
    async def get_profile_repository(self, session: AsyncSession) -> ProfileRepository:
        return ProfileRepository(session=session)
