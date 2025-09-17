from sqlalchemy import event
from sqlalchemy.ext.mutable import MutableComposite, MutableList
from sqlalchemy.orm import composite

from src.db import mapper_registry
from src.modules.profile.domain.profile.aggregate import Profile
from src.modules.profile.domain.profile.value_objects.age import Age
from src.modules.profile.domain.profile.value_objects.bio import Bio
from src.modules.profile.domain.profile.value_objects.city import City
from src.modules.profile.domain.profile.value_objects.media import Media, MediaType
from src.modules.profile.domain.profile.value_objects.name import Name
from src.modules.profile.domain.profile.value_objects.rank import Rank
from src.modules.profile.infra.db.tables import profile_table


class MediaList(MutableComposite, MutableList):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if len(args) == 0:
            return
        self.clear()

        raw_media = args[0]
        if not isinstance(raw_media, list):
            return

        for item in raw_media:
            if isinstance(item, Media):
                self.append(item)
                continue

            file_id = item.get("file_id", None)
            file_type = item.get("media_type", None)
            if file_id is None or file_type is None:
                continue
            try:
                media_type = MediaType(file_type)
            except ValueError:
                continue

            self.append(
                Media(
                    file_id=file_id,
                    media_type=media_type,
                )
            )

    def __composite_values__(self):
        raw_media = []
        for item in self:
            raw_media.append(
                {
                    "file_id": item.file_id,
                    "media_type": item.media_type.value,
                }
            )
        return (raw_media,)


def map_entities() -> None:
    Bio.__composite_values__ = lambda self: (self.description,)

    mapper_registry.map_imperatively(
        Profile,
        profile_table,
        properties={
            "_user_id": profile_table.c.user_id,
            "_name": composite(Name, profile_table.c.name),
            "__name": profile_table.c.name,
            "_city": composite(City, profile_table.c.city),
            "__city": profile_table.c.city,
            "_age": composite(Age, profile_table.c.age),
            "__age": profile_table.c.age,
            "_rank": composite(Rank, profile_table.c.rank),
            "__rank": profile_table.c.rank,
            "_sex": profile_table.c.sex,
            "_bio": composite(lambda v: Bio(v) if v else None, profile_table.c.bio),
            "__bio": profile_table.c.bio,
            "_is_active": profile_table.c.is_active,
            "_interest": profile_table.c.interest,
            "_profile_cursor": profile_table.c.profile_cursor,
            "_rank_cursor": profile_table.c.rank_cursor,
            "_media": composite(MediaList, profile_table.c.media),
            "__media": profile_table.c.media,
        },
        column_prefix="_",
    )

    @event.listens_for(Profile, "load")
    def receive_load(target, context):
        target._domain_events = []
