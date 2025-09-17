from dataclasses import dataclass

from src.modules.profile.domain.profile.errors import NameTooLongError
from src.settings.const import MAX_NAME_LEN
from src.common.domain.value_object import ValueObject


@dataclass(frozen=True)
class Name(ValueObject):

    name: str

    def __str__(self) -> str:
        return self.name

    @classmethod
    def create(cls, name: str) -> "Name":
        if len(name) > MAX_NAME_LEN:
            raise NameTooLongError
        return cls(name=name)
