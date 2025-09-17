from dataclasses import dataclass

from src.common.domain.value_object import ValueObject


@dataclass(frozen=True)
class City(ValueObject):

    city: str

    def __str__(self) -> str:
        return self.city

    @classmethod
    def create(cls, city: str) -> "City":
        return cls(city=city)
