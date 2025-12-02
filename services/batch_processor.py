from models.student import Student

class BatchProcessor:

    @staticmethod
    def batch_enroll(uni, filepath, logger):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # faculty;field;id;name;email
                parts = line.split(";")
                if len(parts) != 5:
                    print(f"Invalid format: {line}")
                    continue

                faculty_name, field, sid, name, email = parts

                if not uni.get_faculty(faculty_name):
                    uni.create_faculty(faculty_name, field)
                    logger.log(f"Batch: created faculty {faculty_name}")

                fac = uni.get_faculty(faculty_name)

                if fac.add_student(Student(sid, name, email)):
                    logger.log(f"Batch: enrolled student {sid} to {faculty_name}")
                else:
                    print(f"Duplicate student `{sid}` or `{email}`")

    @staticmethod
    def batch_graduate(uni, filepath, logger):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                # faculty;idOrEmail
                line = line.strip()
                parts = line.split(";")

                if len(parts) != 2:
                    print(f"Invalid format: {line}")
                    continue

                faculty_name, id_or_email = parts

                fac = uni.get_faculty(faculty_name)
                if not fac:
                    print(f"Faculty `{faculty_name}` not found")
                    continue

                if fac.graduate_student(id_or_email):
                    logger.log(f"Batch: graduated student {id_or_email} from {faculty_name}")
                else:
                    print(f"Cannot graduate `{id_or_email}` — not found")
