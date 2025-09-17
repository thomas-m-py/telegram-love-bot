from dataclasses import dataclass

from stories import Story, I, State, Variable, Argument

from src.modules.match.domain.match.aggregate import Match
from src.modules.match.domain.match.errors import MatchCreationNotAllowedError
from src.modules.match.domain.match.repository import IMatchRepository
from src.modules.match.domain.match.services import CanCreateMatch
from src.modules.match.domain.match.value_objects.message import Message
from src.modules.user.domain.types import TUserId


class CreateMatchState(State):
    from_profile_id: TUserId = Argument()
    to_profile_id: TUserId = Argument()
    message: Message | None = Argument()

    match: Match = Variable()


@dataclass
class CreateMatchCase(Story):

    I.check_can_create_match
    I.create_match
    I.save

    async def check_can_create_match(self, state: CreateMatchState):
        can = await CanCreateMatch(self.match_repository).can(
            state.from_profile_id, state.to_profile_id
        )
        if not can:
            raise MatchCreationNotAllowedError

    async def create_match(self, state: CreateMatchState):
        match_id = await self.match_repository.get_next_id()
        new_match = Match.create(
            match_id=match_id,
            from_profile_id=state.from_profile_id,
            to_profile_id=state.to_profile_id,
            message=state.message,
        )
        state.match = new_match

    async def save(self, state: CreateMatchState):
        self.match_repository.add(state.match)
        await self.match_repository.save(state.match)

    match_repository: IMatchRepository
