from models.llm import generate

class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, query, context, answer):
        
        prompt = f"""
you are an AI evaluator.
score the answer based on:

1. Relevance: (0-10)
2. Faithfulness: (0-10)
3. Correctness: (0-10)

context:
{context}

Question:
{query}

Answer:
{answer}

Return ONLY this format:
Relevance: x
Faithfulness: x
Correctness: x
"""
        result = generate(prompt)
        return result