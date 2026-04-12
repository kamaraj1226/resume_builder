from enum import Enum


class StreamMode(Enum):
    updates: str = "updates"
    custom: str = "custom"
    messages: str = "messages"


class DecisionType(Enum):
    reject: str = "reject"
    approve: str = "approve"


class AvailableModel(Enum):
    qwen_3_5_0_8_b: str = "qwen3.5:0.8b"
    qwen_3_5_4_b: str = "qwen3.5:4b"