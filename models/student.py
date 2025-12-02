class Student:
    def __init__(self, student_id: str, name: str, email: str, graduated=False):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.graduated = graduated

    def graduate(self):
        self.graduated = True

    def to_dict(self):
        return {
            "id": self.student_id,
            "name": self.name,
            "email": self.email,
            "graduated": self.graduated
        }

    @staticmethod
    def from_dict(data):
        return Student(
            student_id=data["id"],
            name=data["name"],
            email=data["email"],
            graduated=data["graduated"]
        )
