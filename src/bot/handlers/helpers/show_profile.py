from aiogram.utils.media_group import MediaGroupBuilder

from src.modules.profile.domain.profile.aggregate import Profile


DEFAULT_MEDIA = [
    ("https://metallps.ru/assets/cache_image/empty_720x540_e0a.png", "photo"),
]


def build_profile(profile_info: Profile | dict) -> MediaGroupBuilder:
    profile = profile_info
    if isinstance(profile_info, Profile):
        media = []
        for m in profile_info.media:
            media.append((m.file_id, m.media_type.value.lower()))

        profile = {
            "name": str(profile_info.name),
            "age": str(int(profile_info.age)),
            "city": str(profile_info.city),
            "bio": str(profile_info.bio) if profile_info.bio else None,
            "media": media,
        }

    caption = f"{profile['name']}, {profile['age']}, {profile['city']}"

    if profile["bio"]:
        caption += f" - {profile['bio']}"

    album = MediaGroupBuilder(caption=caption)

    media = profile.get("media")
    if len(media) == 0:
        media = DEFAULT_MEDIA
    for file_id, media_type in media:
        album.add(type=media_type, media=file_id)

    return album
