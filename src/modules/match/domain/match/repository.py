import abc
from datetime import datetime

from src.modules.match.domain.match.aggregate import Match
from src.modules.match.domain.types import MatchId
from src.modules.user.domain.types import TUserId


class IMatchRepository:

    @abc.abstractmethod
    def add(self, match: Match) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def save(self, match: Match) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, match: Match) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_next_id(self) -> MatchId:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_count_unseen_matches(self, user_id: TUserId) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_first_match_unseen(self, profile_id: TUserId) -> Match | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_by_id(self, match_id: MatchId) -> Match | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_last(
        self, from_profile_id: TUserId, to_profile_id: TUserId
    ) -> Match | None:
        raise NotImplementedError
