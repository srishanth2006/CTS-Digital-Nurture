-- ==========================================
-- Hands-On 3 : Advanced SQL
-- Subqueries, Views & Transactions
-- ==========================================

USE college_db;

-- ==========================================
-- STEP 35
-- Students enrolled in more courses than average
-- ==========================================

SELECT
    s.student_id,
    s.first_name,
    s.last_name,
    COUNT(e.course_id) AS total_courses
FROM students s
JOIN enrollments e
ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.course_id) >
(
    SELECT AVG(course_count)
    FROM
    (
        SELECT COUNT(*) AS course_count
        FROM enrollments
        GROUP BY student_id
    ) avg_table
);

-- ==========================================
-- STEP 36
-- Courses where every enrolled student scored A
-- ==========================================

SELECT c.course_name
FROM courses c
WHERE NOT EXISTS
(
    SELECT *
    FROM enrollments e
    WHERE e.course_id = c.course_id
      AND e.grade <> 'A'
);

-- ==========================================
-- STEP 37
-- Highest paid professor in each department
-- ==========================================

SELECT
    d.dept_name,
    p.prof_name,
    p.salary
FROM professors p
JOIN departments d
ON p.department_id = d.department_id
WHERE p.salary =
(
    SELECT MAX(salary)
    FROM professors
    WHERE department_id = p.department_id
);

-- ==========================================
-- STEP 38
-- Departments whose average salary exceeds 85000
-- ==========================================

SELECT dept_name,
       avg_salary
FROM
(
    SELECT
        d.department_id,
        d.dept_name,
        AVG(p.salary) AS avg_salary
    FROM departments d
    JOIN professors p
    ON d.department_id = p.department_id
    GROUP BY d.department_id, d.dept_name
) dept_avg
WHERE avg_salary > 85000;

-- ==========================================
-- STEP 39
-- View : Student Enrollment Summary
-- ==========================================

CREATE OR REPLACE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name,' ',s.last_name) AS student_name,
    d.dept_name,
    COUNT(e.course_id) AS courses_enrolled,
    ROUND(
        AVG(
            CASE
                WHEN e.grade='A' THEN 4
                WHEN e.grade='B' THEN 3
                WHEN e.grade='C' THEN 2
                WHEN e.grade='D' THEN 1
                ELSE 0
            END
        ),2
    ) AS gpa
FROM students s
LEFT JOIN departments d
ON s.department_id=d.department_id
LEFT JOIN enrollments e
ON s.student_id=e.student_id
GROUP BY s.student_id, student_name, d.dept_name;

-- ==========================================
-- STEP 40
-- View : Course Statistics
-- ==========================================

CREATE OR REPLACE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.student_id) AS total_enrollments,
    ROUND(
        AVG(
            CASE
                WHEN e.grade='A' THEN 4
                WHEN e.grade='B' THEN 3
                WHEN e.grade='C' THEN 2
                WHEN e.grade='D' THEN 1
                ELSE 0
            END
        ),2
    ) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e
ON c.course_id=e.course_id
GROUP BY c.course_id,c.course_name,c.course_code;

-- ==========================================
-- STEP 41
-- Students with GPA > 3.0
-- ==========================================

SELECT *
FROM vw_student_enrollment_summary
WHERE gpa > 3.0;

-- ==========================================
-- STEP 42
-- Attempt to update aggregate view
-- ==========================================

UPDATE vw_student_enrollment_summary
SET courses_enrolled = 5
WHERE student_id = 1;

-- ==========================================
-- STEP 43
-- Drop and recreate view with CHECK OPTION
-- ==========================================

DROP VIEW IF EXISTS vw_student_enrollment_summary;

CREATE VIEW vw_student_enrollment_summary AS
SELECT
    student_id,
    first_name,
    last_name,
    email
FROM students
WHERE department_id = 1
WITH CHECK OPTION;

-- ==========================================
-- STEP 44
-- Stored Procedure : Enroll Student
-- ==========================================

DELIMITER $$

CREATE PROCEDURE sp_enroll_student
(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_date DATE
)
BEGIN

    IF EXISTS
    (
        SELECT *
        FROM enrollments
        WHERE student_id=p_student_id
        AND course_id=p_course_id
    )
    THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Student already enrolled';
    ELSE
        INSERT INTO enrollments
        (student_id,course_id,enrollment_date)
        VALUES
        (p_student_id,p_course_id,p_date);
    END IF;

END$$

DELIMITER ;

-- ==========================================
-- STEP 45
-- Transfer Student Procedure
-- ==========================================

CREATE TABLE IF NOT EXISTS department_transfer_log
(
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    old_department INT,
    new_department INT,
    transfer_date DATETIME
);

DELIMITER $$

CREATE PROCEDURE sp_transfer_student
(
    IN p_student INT,
    IN p_new_department INT
)
BEGIN

    DECLARE old_dept INT;

    START TRANSACTION;

    SELECT department_id
    INTO old_dept
    FROM students
    WHERE student_id=p_student;

    UPDATE students
    SET department_id=p_new_department
    WHERE student_id=p_student;

    INSERT INTO department_transfer_log
    (student_id,old_department,new_department,transfer_date)
    VALUES
    (
        p_student,
        old_dept,
        p_new_department,
        NOW()
    );

    COMMIT;

END$$

DELIMITER ;

-- ==========================================
-- STEP 46
-- Execute Procedure
-- ==========================================

CALL sp_transfer_student(1,2);

SELECT * FROM department_transfer_log;

-- ==========================================
-- STEP 47
-- Transaction with SAVEPOINT
-- ==========================================

START TRANSACTION;

INSERT INTO enrollments
(student_id,course_id,enrollment_date,grade)
VALUES
(2,2,CURDATE(),'A');

SAVEPOINT sp1;

INSERT INTO enrollments
(student_id,course_id,enrollment_date,grade)
VALUES
(3,3,CURDATE(),'B');

ROLLBACK TO sp1;

COMMIT;

SELECT * FROM enrollments;