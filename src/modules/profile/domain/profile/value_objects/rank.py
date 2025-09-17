from dataclasses import dataclass

from src.common.domain.value_object import ValueObject


@dataclass(frozen=True)
class Rank(ValueObject):

    value: int

    def __int__(self) -> int:
        return self.value

    @classmethod
    def create(cls, value: int) -> 'Rank':
        return cls(value)

    def increase(self, value: int) -> 'Rank':
        return Rank(self.value + value)

    def decrease(self, value: int) -> 'Rank':
        return Rank(self.value - value)
