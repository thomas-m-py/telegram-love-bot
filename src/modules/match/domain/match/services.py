from datetime import timedelta, datetime, UTC

from src.modules.match.domain.match.repository import IMatchRepository
from src.modules.user.domain.types import TUserId
from src.settings.const import RECENT_MATCH_DAYS


class CanCreateMatch:

    def __init__(self, match_repository: IMatchRepository):
        self.repo = match_repository

    async def can(self, from_profile_id: TUserId, to_profile_id: TUserId) -> bool:
        date = datetime.now(UTC) - timedelta(days=RECENT_MATCH_DAYS)
        last_match = await self.repo.find_last(from_profile_id, to_profile_id)
        if last_match is None:
            return True

        if last_match.is_waiting_action():
            return False

        if last_match.created_at > date:
            return False

        return True
