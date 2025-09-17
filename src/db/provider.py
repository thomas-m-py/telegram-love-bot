from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from src.db.session import create_sqla_aengine, get_session_maker


class DbProvider(Provider):
    scope = Scope.APP

    def __init__(self, connection_url: str, show_queries: bool) -> None:
        super().__init__()
        self.connection_url = connection_url
        self.show_queries = show_queries

    @provide
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        engine = create_sqla_aengine(self.connection_url, self.show_queries)
        yield engine
        await engine.dispose(True)

    @provide
    def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return get_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, pool: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session
