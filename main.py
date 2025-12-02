from models.university import University
from services.storage_manager import StorageManager
from services.logger import Logger
from services.batch_processor import BatchProcessor


def read(text):
    return input(text).strip()


def general_operations(uni, logger):
    while True:
        print("\n--- GENERAL OPERATIONS ---")
        print("1. Create faculty")
        print("2. Search faculty of student")
        print("3. Display faculties")
        print("4. Display faculties by field")
        print("0. Back")

        op = read("Choose: ")

        if op == "1":
            name = read("Faculty name: ")
            field = read("Field: ")
            if uni.create_faculty(name, field):
                logger.log(f"Created faculty {name}")
                print("Faculty created.")
            else:
                print("Faculty already exists.")

        elif op == "2":
            key = read("Student ID or email: ")
            f = uni.find_student_faculty(key)
            if f:
                print(f"Student belongs to: {f}")
            else:
                print("Not found.")

        elif op == "3":
            for f in uni.list_faculties():
                fac = uni.get_faculty(f)
                print(f"- {f} [{fac.field}]")

        elif op == "4":
            field = read("Field: ")
            res = uni.list_faculties_by_field(field)
            print("Faculties:", res if res else "None")

        elif op == "0":
            return

        else:
            print("Invalid operation.")


def faculty_operations(uni, logger):
    faculty_name = read("Faculty name: ")
    fac = uni.get_faculty(faculty_name)

    if not fac:
        print("Faculty does not exist.")
        return

    while True:
        print(f"\n--- FACULTY OPERATIONS [{faculty_name}] ---")
        print("1. Create & assign student")
        print("2. Graduate student")
        print("3. Show enrolled students")
        print("4. Show graduates")
        print("5. Check membership")
        print("0. Back")

        op = read("Choose: ")

        if op == "1":
            sid = read("ID: ")
            name = read("Name: ")
            email = read("Email: ")

            from models.student import Student
            if fac.add_student(Student(sid, name, email)):
                logger.log(f"Created student {sid} in {faculty_name}")
                print("Added.")
            else:
                print("Duplicate student.")

        elif op == "2":
            key = read("ID or email: ")
            if fac.graduate_student(key):
                logger.log(f"Graduated student {key} from {faculty_name}")
                print("Graduated.")
            else:
                print("Cannot graduate: not found.")

        elif op == "3":
            print("Enrolled students:")
            for s in fac.enrolled():
                print(f"- {s.student_id} | {s.name} | {s.email}")

        elif op == "4":
            print("Graduates:")
            for s in fac.graduated():
                print(f"- {s.student_id} | {s.name} | {s.email}")

        elif op == "5":
            key = read("ID or email: ")
            print("Yes" if fac.has_student(key) else "No")

        elif op == "0":
            return

        else:
            print("Invalid operation.")


def batch_operations(uni, logger):
    while True:
        print("\n--- BATCH OPERATIONS ---")
        print("1. Batch enroll")
        print("2. Batch graduate")
        print("0. Back")

        op = read("Choose: ")

        if op == "1":
            path = read("File path: ")
            BatchProcessor.batch_enroll(uni, path, logger)

        elif op == "2":
            path = read("File path: ")
            BatchProcessor.batch_graduate(uni, path, logger)

        elif op == "0":
            return

        else:
            print("Invalid operation.")


def main():
    storage = StorageManager()
    logger = Logger()

    uni = storage.load()
    print("System loaded.")

    while True:
        print("\n===== TUM Student Management System =====")
        print("1. General operations")
        print("2. Faculty operations")
        print("3. Batch operations")
        print("4. Save")
        print("5. Exit")

        op = read("Choose: ")

        if op == "1":
            general_operations(uni, logger)

        elif op == "2":
            faculty_operations(uni, logger)

        elif op == "3":
            batch_operations(uni, logger)

        elif op == "4":
            storage.save(uni)
            print("Saved.")

        elif op == "5":
            storage.save(uni)
            print("Saved. Exiting.")
            break

        else:
            print("Invalid operation.")


if __name__ == "__main__":
    main()
