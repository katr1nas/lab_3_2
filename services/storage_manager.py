import json
import os
from models.university import University


class StorageManager:
    def __init__(self, path="data/state.json"):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def save(self, uni: University):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(uni.to_dict(), f, indent=4)

    def load(self) -> University:
        # если файла нет → новая система
        if not os.path.exists(self.path):
            return University()

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # если json невалидный или пустой → новая система
            if not isinstance(data, dict) or "name" not in data:
                return University()

            return University.from_dict(data)

        except Exception:
            # любая ошибка → новая система
            return University()
