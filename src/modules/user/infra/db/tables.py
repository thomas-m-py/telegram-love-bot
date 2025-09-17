from sqlalchemy import (
    DateTime,
    text,
    String,
    Table,
    Column,
    BigInteger,
)

from src.db import mapper_registry


user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("tid", BigInteger, primary_key=True),
    Column("username", String, nullable=True),
    Column("first_name", String, nullable=True),
    Column("last_name", String, nullable=True),
    Column("language", String, nullable=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    ),
)
