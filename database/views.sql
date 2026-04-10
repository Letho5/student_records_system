-- =============================================================================
-- STUDENT RECORDS MANAGEMENT SYSTEM
-- File: database/views.sql
-- Purpose: Defines all database views for reporting and querying.
-- =============================================================================


-- =============================================================================
-- VIEW 1: vw_student_overview
-- Complete student profile including enrollment count,
-- average grade, average GPA and attendance rate.
-- =============================================================================

CREATE OR REPLACE VIEW vw_student_overview AS
SELECT
    s.student_id,
    s.first_name,
    s.last_name,
    s.first_name || ' ' || s.last_name       AS full_name,
    s.email,
    s.program,
    s.year_of_study,
    s.status,
    s.enrollment_date,
    COUNT(DISTINCT e.enrollment_id)          AS total_enrollments,
    ROUND(AVG(g.percentage_score), 2)        AS average_grade,
    ROUND(AVG(g.gpa_value), 2)               AS average_gpa,
    ROUND(
        SUM(CASE WHEN a.status = 'Present'
            THEN 1 ELSE 0 END) * 100.0 /
        NULLIF(COUNT(DISTINCT a.attendance_id), 0)
    , 2)                                     AS attendance_rate
FROM students s
LEFT JOIN enrollments e  ON s.student_id    = e.student_id
LEFT JOIN grades g       ON e.enrollment_id = g.enrollment_id
LEFT JOIN attendance a   ON e.enrollment_id = a.enrollment_id
GROUP BY
    s.student_id, s.first_name, s.last_name,
    s.email, s.program, s.year_of_study,
    s.status, s.enrollment_date;


-- =============================================================================
-- VIEW 2: vw_course_enrollment_summary
-- Shows each course with its current enrollment count
-- and available capacity.
-- =============================================================================

CREATE OR REPLACE VIEW vw_course_enrollment_summary AS
SELECT
    c.course_id,
    c.course_code,
    c.course_name,
    c.department,
    c.credits,
    c.semester,
    c.max_students,
    COUNT(e.enrollment_id)                   AS current_enrollments,
    c.max_students - COUNT(e.enrollment_id)  AS available_spots
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
    AND e.status = 'Active'
GROUP BY
    c.course_id, c.course_code, c.course_name,
    c.department, c.credits, c.semester, c.max_students;


-- =============================================================================
-- VIEW 3: vw_student_grades
-- All grade records with full student and course details.
-- =============================================================================

CREATE OR REPLACE VIEW vw_student_grades AS
SELECT
    g.grade_id,
    s.student_id,
    s.first_name || ' ' || s.last_name       AS full_name,
    s.program,
    c.course_code,
    c.course_name,
    c.department,
    g.letter_grade,
    g.percentage_score,
    g.gpa_value,
    g.date_recorded,
    CASE
        WHEN g.percentage_score >= 90 THEN 'Distinction'
        WHEN g.percentage_score >= 80 THEN 'Merit'
        WHEN g.percentage_score >= 70 THEN 'Pass'
        WHEN g.percentage_score >= 60 THEN 'Below Average'
        ELSE 'Fail'
    END                                      AS performance
FROM grades g
JOIN enrollments e ON g.enrollment_id = e.enrollment_id
JOIN students s    ON e.student_id    = s.student_id
JOIN courses c     ON e.course_id     = c.course_id;


-- =============================================================================
-- VIEW 4: vw_attendance_summary
-- Attendance rate per student per course.
-- =============================================================================

CREATE OR REPLACE VIEW vw_attendance_summary AS
SELECT
    s.student_id,
    s.first_name || ' ' || s.last_name       AS full_name,
    s.program,
    c.course_code,
    c.course_name,
    COUNT(a.attendance_id)                   AS total_sessions,
    SUM(CASE WHEN a.status = 'Present'
        THEN 1 ELSE 0 END)                   AS sessions_present,
    SUM(CASE WHEN a.status = 'Absent'
        THEN 1 ELSE 0 END)                   AS sessions_absent,
    ROUND(
        SUM(CASE WHEN a.status = 'Present'
            THEN 1 ELSE 0 END) * 100.0 /
        NULLIF(COUNT(a.attendance_id), 0)
    , 2)                                     AS attendance_rate,
    CASE
        WHEN ROUND(
            SUM(CASE WHEN a.status = 'Present'
                THEN 1 ELSE 0 END) * 100.0 /
            NULLIF(COUNT(a.attendance_id), 0)
        , 2) >= 90 THEN 'Excellent'
        WHEN ROUND(
            SUM(CASE WHEN a.status = 'Present'
                THEN 1 ELSE 0 END) * 100.0 /
            NULLIF(COUNT(a.attendance_id), 0)
        , 2) >= 75 THEN 'Good'
        WHEN ROUND(
            SUM(CASE WHEN a.status = 'Present'
                THEN 1 ELSE 0 END) * 100.0 /
            NULLIF(COUNT(a.attendance_id), 0)
        , 2) >= 60 THEN 'At Risk'
        ELSE 'Critical'
    END                                      AS attendance_standing
FROM attendance a
JOIN enrollments e ON a.enrollment_id = e.enrollment_id
JOIN students s    ON e.student_id    = s.student_id
JOIN courses c     ON e.course_id     = c.course_id
GROUP BY
    s.student_id, s.first_name, s.last_name,
    s.program, c.course_code, c.course_name;


-- =============================================================================
-- VIEW 5: vw_failing_students
-- Students whose average grade is below 50%.
-- =============================================================================

CREATE OR REPLACE VIEW vw_failing_students AS
SELECT
    student_id,
    full_name,
    program,
    year_of_study,
    status,
    total_enrollments,
    average_grade,
    average_gpa,
    attendance_rate
FROM vw_student_overview
WHERE average_grade < 50
ORDER BY average_grade ASC;


-- =============================================================================
-- VIEW 6: vw_top_performing_students
-- Students whose average grade is 75% or above.
-- =============================================================================

CREATE OR REPLACE VIEW vw_top_performing_students AS
SELECT
    student_id,
    full_name,
    program,
    year_of_study,
    status,
    total_enrollments,
    average_grade,
    average_gpa,
    attendance_rate
FROM vw_student_overview
WHERE average_grade >= 75
ORDER BY average_grade DESC;