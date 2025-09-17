from sqlalchemy import (
    DateTime,
    text,
    String,
    Integer,
    Table,
    Column,
    ForeignKey,
    BigInteger,
    Enum,
)

from src.db import mapper_registry
from src.modules.match.domain.match.value_objects.status import Status


match_table = Table(
    "matches",
    mapper_registry.metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    ),
    Column(
        "from_profile_id",
        BigInteger,
        ForeignKey("profiles.user_id", ondelete="cascade"),
        nullable=False,
    ),
    Column(
        "to_profile_id",
        BigInteger,
        ForeignKey("profiles.user_id", ondelete="cascade"),
        nullable=False,
    ),
    Column("status", Enum(Status), nullable=False),
    Column("message_text", String, nullable=True),
    Column("message_video_file_id", String, nullable=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    ),
)
