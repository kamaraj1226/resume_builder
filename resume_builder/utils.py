import os
from langchain_ollama import ChatOllama
from resume_builder.constants import AvailableModel


def get_ollama_host() -> str:
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    return host


def get_ollama_model_name(model_name: str) -> str:
    if model_name in AvailableModel.__members__:
        return model_name
    raise Exception(f"{model_name} is not available")


def get_ollama_model(model_name: str = AvailableModel.qwen_3_5_0_8_b.value):
    model = ChatOllama(
        model=get_ollama_model_name(model_name=model_name),
        temperature=0.9,
        disable_streaming=False,
    )
    return model


def get_user_input():
    user_input = (
        "can you use read_file tool and"
        "In each step convey what you are doing to the user"
        "After reading the pdf file line by line. I want you to convert this to latex format"
        "and save that file inside the same directory were you read the pdf file"
        "Follow proper extension"
        "Once saved go through the latex file and ensure there is no mistake"
    )
    return user_input
