from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.match.infra.db.match_repository import MatchRepository


class MatchModuleProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.REQUEST)
    async def get_match_repository(self, session: AsyncSession) -> MatchRepository:
        return MatchRepository(session=session)
