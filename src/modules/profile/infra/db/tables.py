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
    Boolean,
)
from sqlalchemy.dialects.postgresql import JSONB

from src.db import mapper_registry
from src.modules.profile.domain.profile.value_objects.sex import Sex


profile_table = Table(
    "profiles",
    mapper_registry.metadata,
    Column(
        "user_id",
        BigInteger,
        ForeignKey("users.tid", ondelete="cascade"),
        primary_key=True,
    ),
    Column("rank", Integer, nullable=False),
    Column("rank_cursor", Integer, nullable=True),
    Column("profile_cursor", BigInteger, nullable=True),
    Column("name", String, nullable=False),
    Column("age", Integer, nullable=False),
    Column("bio", String, nullable=True),
    Column("city", String, nullable=False),
    Column("sex", Enum(Sex), nullable=False),
    Column("is_active", Boolean, nullable=False),
    Column("interest", Enum(Sex), nullable=True),
    Column("media", JSONB, nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    ),
)
