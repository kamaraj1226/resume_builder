from enum import Enum


class StreamMode(Enum):
    updates: str = "updates"
    custom: str = "custom"
    messages: str = "messages"


class DecisionType(Enum):
    reject: str = "reject"
    approve: str = "approve"
