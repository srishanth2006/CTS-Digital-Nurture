
CREATE DATABASE college_db;
USE college_db;



CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credits INT,
    department_id INT,
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    grade CHAR(2),
    FOREIGN KEY (student_id)
        REFERENCES students(student_id),
    FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
);

CREATE TABLE professors (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    prof_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);



INSERT INTO departments(dept_name, hod_name, budget)
VALUES
('Computer Science','Dr. Kumar',500000),
('Information Technology','Dr. Priya',400000),
('Electronics','Dr. Raj',350000);

INSERT INTO students(first_name,last_name,email,department_id)
VALUES
('Sri','Shanth','sri@gmail.com',1),
('Rahul','Kumar','rahul@gmail.com',2),
('Anjali','Sharma','anjali@gmail.com',1);

INSERT INTO courses(course_name,credits,department_id)
VALUES
('Database Management',4,1),
('Java Programming',3,1),
('Computer Networks',4,2);

INSERT INTO enrollments(student_id,course_id,grade)
VALUES
(1,1,'A'),
(2,3,'B'),
(3,2,'A');

INSERT INTO professors(prof_name,email,department_id,salary)
VALUES
('Dr. Sharma','sharma@gmail.com',1,75000),
('Dr. Kumar','kumar@gmail.com',2,72000),
('Dr. Singh','singh@gmail.com',3,70000);


SELECT * FROM departments;
SELECT * FROM students;
SELECT * FROM courses;
SELECT * FROM professors;
SELECT * FROM enrollments;



UPDATE professors
SET salary = salary + 5000
WHERE professor_id > 0;



DELETE FROM enrollments
WHERE grade='B';


SELECT
s.first_name,
c.course_name,
e.grade
FROM students s
JOIN enrollments e
ON s.student_id=e.student_id
JOIN courses c
ON e.course_id=c.course_id;


SELECT * FROM departments;
SELECT * FROM students;
SELECT * FROM courses;
SELECT * FROM professors;
SELECT * FROM enrollments;