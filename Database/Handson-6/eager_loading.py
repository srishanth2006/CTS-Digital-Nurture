from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Student

DATABASE_URL = "mysql+pymysql://root:1234@localhost/college_db"

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

print("=== Eager Loading Demo ===")

students = (
    session.query(Student)
    .options(joinedload(Student.department))
    .all()
)

for student in students:
    print(f"{student.first_name} {student.last_name}")

    if student.department:
        print("Department:", student.department.dept_name)

session.close()