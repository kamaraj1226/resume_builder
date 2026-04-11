import ollama
import os


def get_ollama_host()-> str:
    host = os.getenv('OLLAMA_HOST', "http://localhost:11434")
    return host

def get_ollama_model()-> str:
    return "qwen3.5:0.8b"

def main():
    ollama_host = get_ollama_host()
    client = ollama.Client(host=ollama_host)
    model_name = get_ollama_model()
    response = client.chat(model=model_name, messages=[{'role': 'user', 'content': 'Hello!'}])
    print(response)


if __name__ == "__main__":
    main()
