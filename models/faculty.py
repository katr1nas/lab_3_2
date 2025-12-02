from .student import Student

class Faculty:
    def __init__(self, name: str, field: str):
        self.name = name
        self.field = field
        self.students: list[Student] = []

    def add_student(self, student: Student) -> bool:
        for s in self.students:
            if s.student_id == student.student_id or s.email == student.email:
                return False
        self.students.append(student)
        return True

    def graduate_student(self, id_or_email: str) -> bool:
        for s in self.students:
            if s.student_id == id_or_email or s.email == id_or_email:
                s.graduate()
                return True
        return False

    def has_student(self, id_or_email: str) -> bool:
        for s in self.students:
            if s.student_id == id_or_email or s.email == id_or_email:
                return True
        return False

    def enrolled(self):
        return [s for s in self.students if not s.graduated]

    def graduated(self):
        return [s for s in self.students if s.graduated]

    def to_dict(self):
        return {
            "name": self.name,
            "field": self.field,
            "students": [s.to_dict() for s in self.students]
        }

    @staticmethod
    def from_dict(data):
        f = Faculty(data["name"], data["field"])
        for s in data["students"]:
            f.students.append(Student.from_dict(s))
        return f
