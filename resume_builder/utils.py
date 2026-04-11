import os
from langchain_ollama import ChatOllama

def get_ollama_host()-> str:
    host = os.getenv('OLLAMA_HOST', "http://localhost:11434")
    return host

def get_ollama_model_name()-> str:
    return "qwen3.5:0.8b"


def get_ollama_model():
    model = ChatOllama(
        model=get_ollama_model_name(),
        temperature=0.9,
        disable_streaming=False
    )
    return model

