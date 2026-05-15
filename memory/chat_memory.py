from collections import deque

class ChatMemory:
    def __init__(self, size=10):
        self.memory = deque(maxlen=size)

    def add(self, user, response):
        self.memory.append({
            "user": user,
            "response": response
        })

    def get(self):
        return list(self.memory)
