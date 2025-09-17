from dishka import make_async_container

from src.db.provider import DbProvider
from src.modules.user.container import UserModuleProvider
from src.modules.profile.container import (
    ProfileModuleProvider,
)
from src.modules.match.container import MatchModuleProvider

from src.settings.secrets import secrets


di_container = make_async_container(
    DbProvider(
        connection_url=secrets.POSTGRES_URL,
        show_queries=secrets.SHOW_SQL_ALCHEMY_QUERIES,
    ),
    UserModuleProvider(),
    ProfileModuleProvider(),
    MatchModuleProvider(),
)
