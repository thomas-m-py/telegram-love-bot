from src.common.domain.exception import DomainError


class MatchCreationNotAllowedError(DomainError):

    message = "Нельзя создать мэтч"


class CannotMatchRejectedError(DomainError):

    message = "Нельзя замэтчить"


class CannotRejectMatchedError(DomainError):

    message = "Нельзя отклонить"


class MatchNotFoundError(DomainError):

    message = "Мэтч не найден"
