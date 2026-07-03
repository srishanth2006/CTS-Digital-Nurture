import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="college_db"
)

cursor = conn.cursor()

query_count = 0

# Query 1
cursor.execute("SELECT student_id, course_id FROM enrollments")
query_count += 1

enrollments = cursor.fetchall()

for enrollment in enrollments:
    student_id = enrollment[0]

    cursor.execute(
        "SELECT first_name, last_name FROM students WHERE student_id=%s",
        (student_id,)
    )
    query_count += 1

    student = cursor.fetchone()
    print(student)

print("Total Queries Executed:", query_count)

cursor.close()
conn.close()