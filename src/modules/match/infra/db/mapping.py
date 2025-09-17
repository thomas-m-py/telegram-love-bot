from sqlalchemy import event
from sqlalchemy.orm import composite

from src.db import mapper_registry
from src.modules.match.domain.match.aggregate import Match
from src.modules.match.domain.match.value_objects.message import Message, MessageVideo
from src.modules.match.infra.db.tables import match_table


def load_message(text: str | None, video_file_id: str | None) -> Message | None:
    if text is None and video_file_id is None:
        return
    return Message(
        text=text,
        video=MessageVideo(file_id=video_file_id) if video_file_id else None,
    )


def map_entities() -> None:

    Message.__composite_values__ = lambda self: (
        self.text,
        self.video.file_id if self.video else None,
    )

    mapper_registry.map_imperatively(
        Match,
        match_table,
        properties={
            "_match_id": match_table.c.id,
            "_from_profile_id": match_table.c.from_profile_id,
            "_to_profile_id": match_table.c.to_profile_id,
            "_status": match_table.c.status,
            "_message": composite(
                load_message,
                match_table.c.message_text,
                match_table.c.message_video_file_id,
            ),
            "_created_at": match_table.c.created_at,
        },
        column_prefix="_",
    )

    @event.listens_for(Match, "load")
    def receive_load(target, context):
        target._domain_events = []
