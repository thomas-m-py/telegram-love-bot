from dataclasses import dataclass

from src.common.domain.value_object import ValueObject


@dataclass(frozen=True)
class MessageVideo(ValueObject):

    file_id: str

    def __str__(self) -> str:
        return self.file_id

    @classmethod
    def create(cls, file_id: str) -> "MessageVideo":
        return cls(file_id=file_id)


@dataclass(frozen=True)
class Message(ValueObject):

    text: str | None
    video: MessageVideo | None

    def __str__(self) -> str:
        if self.video:
            return str(self.video)
        if self.text:
            return self.text

    def is_video(self) -> bool:
        if self.video:
            return True
        return False

    def is_text(self) -> bool:
        if self.text:
            return True
        return False

    @classmethod
    def create(cls, message: str | MessageVideo) -> "Message":
        if isinstance(message, str):
            return cls(text=message, video=None)
        if isinstance(message, MessageVideo):
            return cls(text=None, video=message)

        raise ValueError("Cannot create message from unknown type")
