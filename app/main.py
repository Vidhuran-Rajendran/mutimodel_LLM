from retrieval.search import HybridSearch
from ingestion.pdf_ingestor import load_pdf
from models.llm import generate

def main():
    print("Multimodal AI System (RAG Enabled)")

    vs = HybridSearch()

    # ✅ Load and index data (ONE TIME)
    filepath = r"data\raw\research_test_file.pdf"
    docs = load_pdf(filepath)
    vs.index(docs)

    print("Documents indexed!")

    while True:
        query = input(">> ")

        if query.lower() == "exit":
            break

        results = vs.search(query)
        print("doc retrived")

        context = "\n".join(map(str, results))
        #context = "\n".join([doc if isinstance(doc, str) else doc[0] for doc in results])
        print("generating ans")

        prompt = f"""
        Answer based on context only:
        Context:{context}
        Question:{query}"""

        response = generate(prompt)

        print("\n", response)


if __name__ == "__main__":
    main()