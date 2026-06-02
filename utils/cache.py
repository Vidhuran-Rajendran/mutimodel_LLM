import json
import os
import hashlib

class Cache:
    def __init__(self, path="cache/cache.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok =True)
        
        if not os.path.exists(self.path):
            with open(self.path, "w")as f:
                json.dump({},f)
    
    def _get_key(self, text):
        return hashlib.md5(text.encode()).hexdigest()
    
    def get(self, text):
        key = self._get_key(text)
        with open(self.path, "r") as f:
            data = json.load(f)
        return data.get(key)

    def set(self, text, value):
        key = self._get_key(text)
        with open(self.path, "r") as f:
            data = json.load(f)
        data[key] = value
        with open(self.path, "w") as f:
            json.dump(data, f,indent=2)