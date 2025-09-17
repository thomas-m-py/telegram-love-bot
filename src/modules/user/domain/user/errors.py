from src.common.domain.exception import DomainError


class UserAlreadyCreatedError(DomainError):

    message = "Пользователь уже создан"


class UserNotFoundError(DomainError):

    message = "Пользователь не найден"
