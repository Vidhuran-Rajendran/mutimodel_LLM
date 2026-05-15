from retrieval.vector_search import HybridSearch
from ingestion.loader import load_text_file
from models.llm import generate

def main():
    print("Multimodal AI System (RAG Enabled)")

    vs = HybridSearch()

    # ✅ Load and index data (ONE TIME)
    filepath = "data/raw/sample.txt"
    docs = load_text_file(filepath)
    vs.index(docs)

    print("Documents indexed!")

    while True:
        query = input(">> ")

        if query.lower() == "exit":
            break

        results = vs.search(query)

        context = "\n".join(map(str, results))
        #context = "\n".join([doc if isinstance(doc, str) else doc[0] for doc in results])

        prompt = f"""
Answer based on context only:

Context:
{context}

Question:
{query}
"""

        response = generate(prompt)

        print("\n", response)


if __name__ == "__main__":
    main()