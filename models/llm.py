import ollama
from utils.cache import Cache

cache = Cache()

def generate(prompt):
    
    cached = cache.get(prompt)
    if cached:
        return cached

    response = ollama.chat(
        model="qwen2.5",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response['message']['content']
    cache.set(prompt, result)
    return result
import ollama

def generate_stream(prompt):
    cached = cache.get(prompt)
    if cached:
        return cached

    stream = ollama.chat(
        model="qwen:latest",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in stream:
        content = chunk["message"]["content"]
        yield content
