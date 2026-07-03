import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="college_db"
)

cursor = conn.cursor()

query = """
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id=e.student_id
JOIN courses c
ON c.course_id=e.course_id;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)

print("Total Queries Executed: 1")

cursor.close()
conn.close()