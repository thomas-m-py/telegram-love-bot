from typing import List

from src.common.domain.entity import Entity
from src.common.domain.event import Event


class RootEntity(Entity):

    _domain_events: List[Event]

    def add_event(self, event: Event):
        self._domain_events.append(event)

    def pull_events(self) -> List[Event]:
        events = self._domain_events or []
        self._domain_events = []
        return events
