import json
import datetime
import os

class Logger:
    def __init__(self, path="logs/history{date.time}.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        
    def log(self,data):
        if not os.path.exists(self.path):
            logs = []
        else:
            with open(self.path, "r") as f:
                logs = json.load(f)
        
        logs.append(data)
        
        with open(self.path, "w")as f:
            json.dump(logs,f,indent=2)
    