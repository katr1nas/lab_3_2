import json
import os
import time


class Logger:
    FILE = "log.txt"

    @staticmethod
    def log(msg):
        with open(Logger.FILE, "a") as f:
            f.write(f"[{time.ctime()}] {msg}\n")



class Student:
    def __init__(self, sid, name, graduated=False):
        self.id = sid
        self.name = name
        self.graduated = graduated

    def to_dict(self):
        return {"id": self.id, "name": self.name, "graduated": self.graduated}

    @staticmethod
    def from_dict(d):
        return Student(d["id"], d["name"], d["graduated"])


class Faculty:
    def __init__(self, name, field):
        self.name = name
        self.field = field
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        Logger.log(f"Enrolled {student.id} to {self.name}")

    def graduate(self, sid):
        for s in self.students:
            if s.id == sid:
                if s.graduated:
                    return False
                s.graduated = True
                Logger.log(f"Graduated {sid} from {self.name}")
                return True
        return False

    def belongs(self, sid):
        return any(s.id == sid for s in self.students)

    def enrolled(self):
        return [s for s in self.students if not s.graduated]

    def graduates(self):
        return [s for s in self.students if s.graduated]

    def to_dict(self):
        return {
            "name": self.name,
            "field": self.field,
            "students": [s.to_dict() for s in self.students]
        }

    @staticmethod
    def from_dict(d):
        fac = Faculty(d["name"], d["field"])
        fac.students = [Student.from_dict(sd) for sd in d["students"]]
        return fac



class SaveManager:
    FILE = "data.json"

    @staticmethod
    def save(faculties):
        data = {name: fac.to_dict() for name, fac in faculties.items()}
        with open(SaveManager.FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load():
        if not os.path.exists(SaveManager.FILE):
            return {}
        with open(SaveManager.FILE, "r") as f:
            data = json.load(f)
        return {name: Faculty.from_dict(fd) for name, fd in data.items()}



def batch_enroll(file, faculties):
    if not os.path.exists(file):
        print("File not found.")
        return

    with open(file) as f:
        for line in f:
            try:
                facname, sid, name = line.strip().split(",")
            except:
                print(f"Invalid format: {line.strip()}")
                continue

            if facname not in faculties:
                print(f"Faculty {facname} does not exist.")
                continue

            faculties[facname].add_student(Student(sid, name))

    Logger.log(f"Batch enrollment from {file}")
    print("Batch enrollment completed.")


def batch_graduate(file, faculties):
    if not os.path.exists(file):
        print("File not found.")
        return

    with open(file) as f:
        for line in f:
            sid = line.strip()
            if not sid:
                continue

            found = False
            for fac in faculties.values():
                if fac.graduate(sid):
                    found = True
                    break

            if not found:
                print(f"Cannot graduate student: {sid} (student not present)")

    Logger.log(f"Batch graduation from {file}")
    print("Batch graduation completed.")



def main():
    faculties = SaveManager.load()

    while True:
        print("\n--- TUM Student Management ---")
        print("1. Create faculty")
        print("2. Assign student to faculty")
        print("3. Graduate student")
        print("4. Show enrolled")
        print("5. Show graduates")
        print("6. Check student in faculty")
        print("7. Search student’s faculty")
        print("8. Show all faculties")
        print("9. Show faculties by field")
        print("10. Batch enroll")
        print("11. Batch graduate")
        print("0. Exit")

        op = input("Choose: ")

        if op == "1":
            name = input("Faculty name: ")
            field = input("Field: ")
            faculties[name] = Faculty(name, field)
            Logger.log(f"Created faculty {name}")

        elif op == "2":
            fac = input("Faculty: ")
            if fac not in faculties:
                print("Faculty not found.")
                continue
            sid = input("Student ID: ")
            name = input("Student name: ")
            faculties[fac].add_student(Student(sid, name))

        elif op == "3":
            sid = input("Student ID: ")
            ok = False
            for fac in faculties.values():
                if fac.graduate(sid):
                    ok = True
                    break
            if not ok:
                print(f"Cannot graduate student: {sid} (student not present)")

        elif op == "4":
            fac = input("Faculty: ")
            if fac not in faculties:
                print("Faculty not found.")
                continue
            for s in faculties[fac].enrolled():
                print(s.id, s.name)

        elif op == "5":
            fac = input("Faculty: ")
            if fac not in faculties:
                print("Faculty not found.")
                continue
            for s in faculties[fac].graduates():
                print(s.id, s.name)

        elif op == "6":
            fac = input("Faculty: ")
            sid = input("Student ID: ")
            if fac not in faculties:
                print("Faculty not found.")
                continue
            print("Yes" if faculties[fac].belongs(sid) else "No")

        elif op == "7":
            sid = input("Student ID: ")
            found = False
            for name, fac in faculties.items():
                if fac.belongs(sid):
                    print("Belongs to:", name)
                    found = True
                    break
            if not found:
                print("Student not found.")

        elif op == "8":
            for name in faculties:
                print(name)

        elif op == "9":
            field = input("Field: ")
            for name, fac in faculties.items():
                if fac.field == field:
                    print(name)

        elif op == "10":
            file = input("File name: ")
            batch_enroll(file, faculties)

        elif op == "11":
            file = input("File name: ")
            batch_graduate(file, faculties)

        elif op == "0":
            SaveManager.save(faculties)
            print("Saved and exit.")
            break

        else:
            print("Invalid operation.")

        SaveManager.save(faculties)


if __name__ == "__main__":
    main()

