import ollama

def generate(prompt):
    response = ollama.chat(
        model="qwen3.5",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']