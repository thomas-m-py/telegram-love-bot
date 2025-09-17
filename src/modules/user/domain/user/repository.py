import abc

from src.modules.user.domain.types import TUserId
from src.modules.user.domain.user.aggregate import User


class IUserRepository:

    @abc.abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def exists_by_tid(self, user_id: TUserId) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_by_tid(self, tid: TUserId) -> User | None:
        raise NotImplementedError
