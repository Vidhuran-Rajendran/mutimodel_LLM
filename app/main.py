from app.router import route
from app.agent import run_agent

def main():
    print("Multimodal AI System Started")

    while True:
        query = input(">> ")

        if query.lower() == "exit":
            break

        task = route(query)

        if task == "rag":
            response = run_agent(query)
        else:
            response = f"{task} module not implemented yet"

        print(response)

if __name__ == "__main__":
    main()