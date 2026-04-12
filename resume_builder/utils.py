import os
from langchain_ollama import ChatOllama
from resume_builder.constants import AvailableModel
from pydantic import BaseModel
from typing import Any, List, Dict
from resume_builder.constants import StreamMode
from langgraph.checkpoint.memory import InMemorySaver
import sys


def get_ollama_host() -> str:
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    return host


def get_ollama_model_name(model_name: AvailableModel) -> str:
    if model_name.name in AvailableModel.__members__:
        return model_name.value
    raise Exception(f"{model_name} is not available")


def get_ollama_model(model_name: str = AvailableModel.qwen_3_5_4_b):
    model = ChatOllama(
        model=get_ollama_model_name(model_name=model_name),
        temperature=0.9,
        disable_streaming=False,
    )
    return model


def get_user_input():
    print("You>> ", end="", flush=True)
    try:
        user_input = sys.stdin.read()
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


class MemoryProvider:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryProvider, cls).__new__(cls)
            cls._instance.checkpointer = InMemorySaver()
        return cls._instance
