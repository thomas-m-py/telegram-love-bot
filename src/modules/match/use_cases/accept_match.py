from dataclasses import dataclass

from stories import Story, I, State, Variable, Argument

from src.modules.match.domain.match.aggregate import Match
from src.modules.match.domain.match.errors import MatchNotFoundError
from src.modules.match.domain.match.repository import IMatchRepository
from src.modules.match.domain.types import MatchId


class AcceptMatchState(State):
    match_id: MatchId = Argument()

    match: Match = Variable()


@dataclass
class AcceptMatchCase(Story):

    I.find_match
    I.accept_match
    I.save

    async def find_match(self, state: AcceptMatchState):
        match = await self.match_repository.find_by_id(state.match_id)
        if match is None:
            raise MatchNotFoundError
        state.match = match

    async def accept_match(self, state: AcceptMatchState):
        state.match.match()

    async def save(self, state: AcceptMatchState):
        await self.match_repository.save(state.match)

    match_repository: IMatchRepository
