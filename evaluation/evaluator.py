from models.llm import generate

class Evaluator:
    def __init__(self):
        pass
    
    def parse(self,text):
        scores = {
            "relevance": 0,
            "faithfulness": 0,
            "correctness": 0    
        }
        for line in text.split("\n"):
            if "Relevance" in line:
                scores["relevance"] = int(line.split(":")[1].strip())
            elif "Faithfulness" in line:
                scores["faithfulness"] = int(line.split(":")[1].strip())
            elif "Correctness" in line:
                scores["correctness"] = int(line.split(":")[1].strip())
        return scores

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
        return self.parse(result)