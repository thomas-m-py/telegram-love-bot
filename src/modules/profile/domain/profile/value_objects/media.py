from dataclasses import dataclass
from enum import Enum

from src.common.domain.value_object import ValueObject


class MediaType(Enum):
    PHOTO = 'PHOTO'
    VIDEO = 'VIDEO'


@dataclass(frozen=True)
class Media(ValueObject):

    file_id: str
    media_type: MediaType

    @classmethod
    def create(cls, file_id: str, media_type: MediaType) -> 'Media':
        return cls(file_id=file_id, media_type=media_type)
