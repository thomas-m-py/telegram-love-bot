from dataclasses import dataclass

from stories import Story, I, State, Variable, Argument

from src.modules.match.domain.match.aggregate import Match
from src.modules.match.domain.match.errors import MatchNotFoundError
from src.modules.match.domain.match.repository import IMatchRepository
from src.modules.match.domain.types import MatchId


class RejectMatchState(State):
    match_id: MatchId = Argument()

    match: Match = Variable()


@dataclass
class RejectMatchCase(Story):

    I.find_match
    I.reject_match
    I.save

    async def find_match(self, state: RejectMatchState):
        match = await self.match_repository.find_by_id(state.match_id)
        if match is None:
            raise MatchNotFoundError
        state.match = match

    async def reject_match(self, state: RejectMatchState):
        state.match.reject()

    async def save(self, state: RejectMatchState):
        await self.match_repository.save(state.match)

    match_repository: IMatchRepository
