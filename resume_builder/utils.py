import os
from langchain_ollama import ChatOllama
from resume_builder.constants import AvailableModel
from pydantic import BaseModel
from typing import Any, List
from resume_builder.constants import StreamMode
from langgraph.checkpoint.memory import InMemorySaver
import sys
from dataclasses import dataclass, field


class SingletonMeta(type):
    """
    Used to handle single ton
    """

    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]


@dataclass(frozen=True)
class GetModel(metaclass=SingletonMeta):
    _model: Any = field(init=False, repr=False)
    model_name: str = AvailableModel.qwen_3_5_0_8_b

    def __post_init__(self):
        model_instance = get_ollama_model_instance(model_name=self.model_name)
        object.__setattr__(self, "_model", model_instance)

    @property
    def model(self):
        return self._model


@dataclass(frozen=True)
class MemoryProvider(metaclass=SingletonMeta):
    _checkpointer: Any = field(init=False, repr=False)

    def __post_init__(self):
        checkpointer = InMemorySaver()
        object.__setattr__(self, "_checkpointer", checkpointer)

    @property
    def checkpointer(self):
        return self._checkpointer


def get_ollama_host() -> str:
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    return host


def get_ollama_model_name(model_name: AvailableModel) -> str:
    if model_name.name in AvailableModel.__members__:
        return model_name.value
    raise Exception(f"{model_name} is not available")


def get_ollama_model(model_name: str = AvailableModel.qwen_3_5_0_8_b):
    model = GetModel(model_name)
    return model.model


def get_ollama_model_instance(model_name: str = AvailableModel.qwen_3_5_0_8_b):
    model = ChatOllama(
        model=get_ollama_model_name(model_name=model_name),
        temperature=0.9,
        disable_streaming=False,
    )
    return model


def get_user_input():
    print("You (press ctrl+d)>> ", end="", flush=True)
    try:
        # user_input = sys.stdin.read()
        user_input = input()  # TODO: temporary override
        return user_input.strip()
    except EOFError:
        return ""
    except KeyboardInterrupt:
        return "/quit"


class StreamObj(BaseModel):
    agent: Any
    stream_mode: List[str] = [mode.value for mode in StreamMode]
    version: str = "v2"
    show_tool_output: bool = True
