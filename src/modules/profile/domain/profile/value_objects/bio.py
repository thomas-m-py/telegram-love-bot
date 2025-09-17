from dataclasses import dataclass

from src.modules.profile.domain.profile.errors import BioTooShortError, BioTooLongError
from src.settings.const import MIN_BIO_LEN, MAX_BIO_LEN
from src.common.domain.value_object import ValueObject


@dataclass(frozen=True)
class Bio(ValueObject):

    description: str

    def __str__(self) -> str:
        return self.description

    @classmethod
    def create(cls, description: str) -> "Bio":
        if len(description) < MIN_BIO_LEN:
            raise BioTooShortError
        if len(description) > MAX_BIO_LEN:
            raise BioTooLongError

        return cls(description=description)
