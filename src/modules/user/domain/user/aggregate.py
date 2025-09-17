from src.common.domain.aggregate import RootEntity
from src.modules.user.domain.types import TUserId


class User(RootEntity):

    def __init__(
        self,
        user_id: TUserId,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        language: str | None = None,
    ):
        self._domain_events = []

        self._id = user_id
        self._username = username
        self._first_name = first_name
        self._last_name = last_name
        self._language = language

    @property
    def id(self) -> TUserId:
        return self._id

    @property
    def username(self) -> str | None:
        return self._username

    @property
    def first_name(self) -> str | None:
        return self._first_name

    @property
    def last_name(self) -> str | None:
        return self._last_name

    @property
    def language(self) -> str | None:
        return self._language

    @classmethod
    def create(
        cls,
        user_id: TUserId,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        language: str | None = None,
    ):
        return cls(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            language=language,
        )

    def set_lang(self, language: str) -> None:
        self._language = language

    def set_first_name(self, first_name: str) -> None:
        self._first_name = first_name

    def set_last_name(self, last_name: str) -> None:
        self._last_name = last_name

    def set_username(self, username: str) -> None:
        self._username = username
