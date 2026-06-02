import time

class Monitor:

    def __init__(self):
        self.logs = []

    def start(self, name):
        return {"name": name, "start": time.time()}

    def end(self, entry):
        entry["end"] = time.time()
        entry["duration"] = entry["end"] - entry["start"]
        self.logs.append(entry)

    def report(self):
        print("\n---- MONITOR ----")
        for log in self.logs:
            print(f"{log['name']} → {log['duration']:.4f}s")
        print("-----------------\n")
