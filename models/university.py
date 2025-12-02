from .faculty import Faculty

class University:
    def __init__(self, name="Technical University of Moldova"):
        self.name = name
        self.faculties: dict[str, Faculty] = {}

    def create_faculty(self, name: str, field: str) -> bool:
        if name in self.faculties:
            return False
        self.faculties[name] = Faculty(name, field)
        return True

    def get_faculty(self, name: str):
        return self.faculties.get(name)

    def list_faculties(self):
        return list(self.faculties.keys())

    def list_faculties_by_field(self, field: str):
        return [f.name for f in self.faculties.values() if f.field == field]

    def find_student_faculty(self, id_or_email: str):
        for f in self.faculties.values():
            if f.has_student(id_or_email):
                return f.name
        return None

    def to_dict(self):
        return {
            "name": self.name,
            "faculties": {name: f.to_dict() for name, f in self.faculties.items()}
        }

    @staticmethod
    def from_dict(data):
        u = University(data["name"])
        for name, f in data["faculties"].items():
            u.faculties[name] = Faculty.from_dict(f)
        return u
