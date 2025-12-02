import datetime
import os

class Logger:
    def __init__(self, path="data/log.txt"):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def log(self, msg: str):
        with open(self.path, "a", encoding="utf-8") as f:
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{time}] {msg}\n")
