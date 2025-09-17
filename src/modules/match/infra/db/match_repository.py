from sqlalchemy import text, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.match.domain.match.aggregate import Match
from src.modules.match.domain.match.repository import IMatchRepository
from src.modules.match.domain.match.value_objects.status import Status
from src.modules.match.domain.types import MatchId
from src.modules.user.domain.types import TUserId


class MatchRepository(IMatchRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add(self, match: Match) -> None:
        self.session.add(match)

    async def save(self, match: Match) -> None:
        await self.session.commit()

    async def delete(self, match: Match) -> None:
        await self.session.delete(match)

    async def get_next_id(self) -> MatchId:
        stmt = text(
            "Select nextval(pg_get_serial_sequence('matches', 'id')) as new_id;"
        )
        result = await self.session.execute(stmt)
        return MatchId(result.scalar())

    async def get_count_unseen_matches(self, user_id: TUserId) -> int:
        stmt = (
            select(func.count())
            .select_from(Match)
            .where(Match._to_profile_id == user_id)
            .where(Match._status == Status.WAITING_ACTION)
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_first_match_unseen(self, profile_id: TUserId) -> Match | None:
        stmt = (
            select(Match)
            .where(Match._to_profile_id == profile_id)
            .where(Match._status == Status.WAITING_ACTION)
            .order_by(Match._created_at.asc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_id(self, match_id: MatchId) -> Match | None:
        return await self.session.get(Match, match_id)

    async def find_last(
        self, from_profile_id: TUserId, to_profile_id: TUserId
    ) -> Match | None:
        stmt = (
            select(Match)
            .where(Match._to_profile_id == to_profile_id)
            .where(Match._from_profile_id == from_profile_id)
            .order_by(Match._created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
