USE college_db;

INSERT INTO students
(first_name,last_name,email,department_id,enrollment_year)
VALUES
('Arun','Kumar','arun@gmail.com',1,2023);

INSERT INTO students
(first_name,last_name,email,department_id,enrollment_year)
VALUES
('Meena','Ravi','meena2026@gmail.com',2,2023);

UPDATE enrollments
SET grade='B'
WHERE student_id=1
AND course_id=1;

DELETE FROM enrollments
WHERE grade IS NULL;

SELECT COUNT(*) AS department_count
FROM departments;

SELECT COUNT(*) AS student_count
FROM students;

SELECT COUNT(*) AS course_count
FROM courses;

SELECT COUNT(*) AS professor_count
FROM professors;

SELECT COUNT(*) AS enrollment_count
FROM enrollments;

SELECT *
FROM students
WHERE enrollment_year=2022
ORDER BY last_name ASC;

SELECT *
FROM courses
WHERE credits>3
ORDER BY credits DESC;

SELECT *
FROM professors
WHERE salary BETWEEN 80000 AND 95000;

SELECT *
FROM students
WHERE email LIKE '%@college.edu';

SELECT
enrollment_year,
COUNT(*) AS total_students
FROM students
GROUP BY enrollment_year
ORDER BY enrollment_year;

SELECT
CONCAT(s.first_name,' ',s.last_name) AS full_name,
d.dept_name
FROM students s
JOIN departments d
ON s.department_id=d.department_id;

SELECT
CONCAT(s.first_name,' ',s.last_name) AS student_name,
c.course_name,
e.grade
FROM students s
JOIN enrollments e
ON s.student_id=e.student_id
JOIN courses c
ON e.course_id=c.course_id;

SELECT
p.prof_name,
d.dept_name
FROM professors p
JOIN departments d
ON p.department_id=d.department_id;

SELECT
d.dept_name,
COUNT(s.student_id) AS total_students
FROM departments d
LEFT JOIN students s
ON d.department_id=s.department_id
GROUP BY d.department_id,d.dept_name;

SELECT AVG(salary) AS average_salary
FROM professors;

SELECT
MAX(salary) AS highest_salary,
MIN(salary) AS lowest_salary
FROM professors;

SELECT
department_id,
COUNT(*) AS total_professors
FROM professors
GROUP BY department_id;

SELECT SUM(budget) AS total_budget
FROM departments;

SELECT *
FROM departments
WHERE budget=
(
SELECT MAX(budget)
FROM departments
);

SELECT *
FROM students
WHERE department_id=
(
SELECT department_id
FROM departments
WHERE dept_name='Computer Science'
);

SELECT *
FROM professors
WHERE salary>
(
SELECT AVG(salary)
FROM professors
);

SELECT *
FROM courses
WHERE department_id IN
(
SELECT department_id
FROM departments
WHERE budget>400000
);

CREATE VIEW student_department_view AS
SELECT
s.student_id,
CONCAT(s.first_name,' ',s.last_name) AS student_name,
d.dept_name,
s.email
FROM students s
JOIN departments d
ON s.department_id=d.department_id;

SELECT *
FROM student_department_view;

SHOW FULL TABLES
WHERE Table_type='VIEW';

DROP VIEW student_department_view;

SELECT * FROM departments;
SELECT * FROM students;
SELECT * FROM courses;
SELECT * FROM professors;
SELECT * FROM enrollments;