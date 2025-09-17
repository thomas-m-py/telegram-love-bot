from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

from src.modules.user.infra.db.mapping import map_entities as map_user_entities
from src.modules.profile.infra.db.mapping import map_entities as map_profile_entities
from src.modules.match.infra.db.mapping import map_entities as map_match_entities


def create_sqla_aengine(connection_url: str, echo: bool = False) -> AsyncEngine:
    return create_async_engine(connection_url, echo=echo, pool_pre_ping=True)


def get_session_maker(aengine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(aengine, autoflush=False, expire_on_commit=False)


map_user_entities()
map_profile_entities()
map_match_entities()
