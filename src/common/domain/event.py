import uuid
from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID


@dataclass
class Event:
    event_id: UUID = field(default_factory=uuid.uuid4, init=False)
    occurred_at: datetime = field(default_factory=datetime.now, init=False)

    def __post_init__(self):
        self.event_id = uuid.uuid4()
        self.occurred_at = datetime.now(UTC)
