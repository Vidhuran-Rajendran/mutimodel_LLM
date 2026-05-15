import ollama

def generate(prompt):
    response = ollama.chat(
        model="qwen2.5",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']