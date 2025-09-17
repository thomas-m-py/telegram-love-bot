from src.common.domain.exception import DomainError


class AgeRestrictionError(DomainError):

    message = "Возрастное ограничение"


class NotRealAgeError(DomainError):

    message = "Не настоящий возраст"


class BioTooShortError(DomainError):

    message = "Описание слишком короткое"


class BioTooLongError(DomainError):

    message = "Описание слишком длинное"


class NameTooLongError(DomainError):

    message = "Имя слишком длинное"


class MediaLimitExceededError(DomainError):

    message = "Превышен лимит медиа файлов"


class ProfileNotFoundError(DomainError):

    message = "Анкета не найдена"
