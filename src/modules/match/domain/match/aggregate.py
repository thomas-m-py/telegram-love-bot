from datetime import datetime, UTC

from src.common.domain.aggregate import RootEntity
from src.modules.match.domain.match.errors import (
    CannotMatchRejectedError,
    CannotRejectMatchedError,
)
from src.modules.match.domain.match.value_objects.message import Message
from src.modules.match.domain.match.value_objects.status import Status
from src.modules.match.domain.types import MatchId
from src.modules.user.domain.types import TUserId


class Match(RootEntity):

    def __init__(
        self,
        match_id: MatchId,
        from_profile_id: TUserId,
        to_profile_id: TUserId,
        status: Status,
        created_at: datetime,
        message: Message | None = None,
    ):
        self._domain_events = []

        self._match_id = match_id
        self._from_profile_id = from_profile_id
        self._to_profile_id = to_profile_id
        self._status = status
        self._message = message
        self._created_at = created_at

    @property
    def match_id(self) -> MatchId:
        return self._match_id

    @property
    def from_profile_id(self) -> TUserId:
        return self._from_profile_id

    @property
    def to_profile_id(self) -> TUserId:
        return self._to_profile_id

    @property
    def status(self) -> Status:
        return self._status

    @property
    def message(self) -> Message | None:
        return self._message

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @classmethod
    def create(
        cls,
        match_id: MatchId,
        from_profile_id: TUserId,
        to_profile_id: TUserId,
        message: Message | None = None,
    ) -> "Match":
        return cls(
            match_id,
            from_profile_id,
            to_profile_id,
            Status.WAITING_ACTION,
            datetime.now(UTC),
            message,
        )

    def match(self) -> None:
        if self._status == Status.REJECTED:
            raise CannotMatchRejectedError

        self._status = Status.MATCHED

    def reject(self) -> None:
        if self._status == Status.MATCHED:
            raise CannotRejectMatchedError

        self._status = Status.REJECTED

    def is_waiting_action(self) -> bool:
        return self._status == Status.WAITING_ACTION

    def is_rejected(self) -> bool:
        return self._status == Status.REJECTED

    def is_matched(self) -> bool:
        return self._status == Status.MATCHED
