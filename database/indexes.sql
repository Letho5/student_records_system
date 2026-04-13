-- =============================================================================
-- STUDENT RECORDS MANAGEMENT SYSTEM
-- File: database/indexes.sql
-- Purpose: Creates indexes to optimise query performance.
-- =============================================================================


-- =============================================================================
-- STUDENTS TABLE INDEXES
-- =============================================================================

-- Index on email — frequently searched and must be unique
CREATE INDEX IF NOT EXISTS idx_students_email
    ON students(email);

-- Index on status — used in filtering queries
CREATE INDEX IF NOT EXISTS idx_students_status
    ON students(status);

-- Index on program — used in filtering and grouping
CREATE INDEX IF NOT EXISTS idx_students_program
    ON students(program);

-- Index on year_of_study — used in filtering queries
CREATE INDEX IF NOT EXISTS idx_students_year
    ON students(year_of_study);


-- =============================================================================
-- COURSES TABLE INDEXES
-- =============================================================================

-- Index on course_code — frequently searched
CREATE INDEX IF NOT EXISTS idx_courses_code
    ON courses(course_code);

-- Index on department — used in filtering and grouping
CREATE INDEX IF NOT EXISTS idx_courses_department
    ON courses(department);

-- Index on semester — used in filtering queries
CREATE INDEX IF NOT EXISTS idx_courses_semester
    ON courses(semester);


-- =============================================================================
-- ENROLLMENTS TABLE INDEXES
-- =============================================================================

-- Index on student_id — used in every JOIN with students
CREATE INDEX IF NOT EXISTS idx_enrollments_student
    ON enrollments(student_id);

-- Index on course_id — used in every JOIN with courses
CREATE INDEX IF NOT EXISTS idx_enrollments_course
    ON enrollments(course_id);

-- Index on status — used in filtering queries
CREATE INDEX IF NOT EXISTS idx_enrollments_status
    ON enrollments(status);

-- Index on enrollment_date — used in date range queries
CREATE INDEX IF NOT EXISTS idx_enrollments_date
    ON enrollments(enrollment_date);


-- =============================================================================
-- GRADES TABLE INDEXES
-- =============================================================================

-- Index on enrollment_id — used in every JOIN with enrollments
CREATE INDEX IF NOT EXISTS idx_grades_enrollment
    ON grades(enrollment_id);

-- Index on letter_grade — used in filtering queries
CREATE INDEX IF NOT EXISTS idx_grades_letter
    ON grades(letter_grade);

-- Index on percentage_score — used in range queries
CREATE INDEX IF NOT EXISTS idx_grades_score
    ON grades(percentage_score);


-- =============================================================================
-- ATTENDANCE TABLE INDEXES
-- =============================================================================

-- Index on enrollment_id — used in every JOIN with enrollments
CREATE INDEX IF NOT EXISTS idx_attendance_enrollment
    ON attendance(enrollment_id);

-- Index on attendance_date — used in date range queries
CREATE INDEX IF NOT EXISTS idx_attendance_date
    ON attendance(attendance_date);

-- Index on status — used in filtering queries
CREATE INDEX IF NOT EXISTS idx_attendance_status
    ON attendance(status);


-- =============================================================================
-- COMPOSITE INDEXES
-- These cover queries that filter on multiple columns simultaneously
-- =============================================================================

-- Composite index on enrollments — student and course together
CREATE INDEX IF NOT EXISTS idx_enrollments_student_course
    ON enrollments(student_id, course_id);

-- Composite index on attendance — enrollment and date together
CREATE INDEX IF NOT EXISTS idx_attendance_enrollment_date
    ON attendance(enrollment_id, attendance_date);