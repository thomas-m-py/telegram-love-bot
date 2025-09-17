from sqlalchemy import event

from src.db import mapper_registry
from src.modules.user.domain.user.aggregate import User
from src.modules.user.infra.db.tables import user_table


def map_entities() -> None:

    mapper_registry.map_imperatively(
        User,
        user_table,
        properties={
            "_id": user_table.c.tid,
            "_username": user_table.c.username,
            "_first_name": user_table.c.first_name,
            "_last_name": user_table.c.last_name,
            "_language": user_table.c.language,
        },
        column_prefix="_",
    )

    @event.listens_for(User, "load")
    def receive_load(target, context):
        target._domain_events = []
