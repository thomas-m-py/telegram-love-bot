from enum import Enum


class Status(Enum):

    WAITING_ACTION = "WAITING_ACTION"
    REJECTED = "REJECTED"
    MATCHED = "MATCHED"
