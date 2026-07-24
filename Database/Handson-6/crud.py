from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Department

DATABASE_URL = "mysql+pymysql://root:1234@localhost/college_db"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

# -------------------------------
# CREATE
# -------------------------------
new_student = Student(
    first_name="John",
    last_name="Doe",
    email="john.doe@gmail.com",
    department_id=1
)

session.add(new_student)
session.commit()

print("Student inserted successfully.")

# -------------------------------
# READ
# -------------------------------
print("\nStudents List")
students = session.query(Student).all()

for s in students:
    print(s.student_id, s.first_name, s.last_name, s.email)

# -------------------------------
# UPDATE
# -------------------------------
student = session.query(Student).filter_by(student_id=new_student.student_id).first()

if student:
    student.last_name = "Smith"
    session.commit()
    print("\nStudent updated successfully.")

# -------------------------------
# DELETE
# -------------------------------
student = session.query(Student).filter_by(student_id=new_student.student_id).first()

if student:
    session.delete(student)
    session.commit()
    print("Student deleted successfully.")

session.close()