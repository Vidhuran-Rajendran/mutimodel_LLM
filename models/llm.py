import ollama

def generate(prompt):
    response = ollama.chat(
        model="qwen2.5",
        messages=[{"role": "user", "content": prompt}]
    )
    print("generating responce")
    return response['message']['content']