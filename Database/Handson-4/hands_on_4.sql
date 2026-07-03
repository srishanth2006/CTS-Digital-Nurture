-- ==========================================
-- Hands-On 4
-- Query Optimization and Performance Tuning
-- ==========================================

USE college_db;

-- ==========================================
-- STEP 48
-- Analyze Query Execution Plan
-- ==========================================

EXPLAIN FORMAT=JSON
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE YEAR(e.enrollment_date) = 2022;

-- ==========================================
-- STEP 49
-- Analyze Simple Query
-- ==========================================

EXPLAIN
SELECT *
FROM students;

-- ==========================================
-- STEP 50
-- Observations
-- ==========================================

-- The execution plans were analyzed using EXPLAIN.
-- This helps identify whether MySQL performs
-- table scans or uses indexes.

-- ==========================================
-- STEP 51
-- Create Index on Enrollment Year
-- ==========================================

CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);

-- ==========================================
-- STEP 52
-- Composite Unique Index
-- ==========================================

CREATE UNIQUE INDEX idx_enrollment_student_course
ON enrollments(student_id, course_id);

-- ==========================================
-- STEP 53
-- Index on Course Code
-- ==========================================

CREATE INDEX idx_course_code
ON courses(course_code);

-- ==========================================
-- STEP 54
-- Compare Execution Plan After Indexing
-- ==========================================

EXPLAIN FORMAT=JSON
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE YEAR(e.enrollment_date) = 2022;

-- ==========================================
-- STEP 55
-- Additional Index
-- ==========================================

CREATE INDEX idx_enrollment_student
ON enrollments(student_id);

-- MySQL Community Edition does not support
-- PostgreSQL-style partial indexes with
-- WHERE conditions. A regular index is used.

-- ==========================================
-- STEP 56
-- N+1 Query Problem
-- ==========================================

-- Refer to:
-- n_plus_one.py

-- ==========================================
-- STEP 57
-- Optimized JOIN Version
-- ==========================================

-- Refer to:
-- optimized_join.py

-- ==========================================
-- STEP 58
-- Analysis
-- ==========================================

-- N+1 Query:
-- One query retrieves all enrollments and
-- an additional query is executed for each
-- student record.

-- Optimized JOIN:
-- Retrieves all required data using a
-- single JOIN query.

-- ==========================================
-- STEP 59
-- Performance Comparison
-- ==========================================

-- If there are 10,000 enrollments:

-- N+1 Approach
-- Total Queries = 10,001

-- JOIN Approach
-- Total Queries = 1

-- The JOIN approach minimizes database
-- round trips and significantly improves
-- application performance.

-- ==========================================
-- Verification
-- ==========================================

SHOW INDEX FROM students;

SHOW INDEX FROM courses;

SHOW INDEX FROM enrollments;