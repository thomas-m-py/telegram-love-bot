from dataclasses import dataclass

from src.modules.user.domain.types import TUserId


@dataclass
class CreateUserDTO:

    tid: TUserId
    first_name: str | None
    last_name: str | None
    username: str | None
    language: str | None


@dataclass
class UpdateUserDTO:
    tid: TUserId
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    language: str | None = None
