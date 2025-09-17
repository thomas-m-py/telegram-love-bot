from dataclasses import dataclass

from src.modules.profile.domain.profile.errors import (
    AgeRestrictionError,
    NotRealAgeError,
)
from src.settings.const import AGE_RESTRICTION, NOT_REAL_AGE
from src.common.domain.value_object import ValueObject


@dataclass(frozen=True)
class Age(ValueObject):

    value: int

    def __int__(self) -> int:
        return self.value

    @classmethod
    def create(cls, age: int) -> "Age":
        if age < AGE_RESTRICTION:
            raise AgeRestrictionError

        if age >= NOT_REAL_AGE:
            raise NotRealAgeError

        return cls(age)
