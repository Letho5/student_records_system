-- =============================================================================
-- STUDENT RECORDS MANAGEMENT SYSTEM
-- File: database/procedures.sql
-- Purpose: Defines all stored procedures for system operations.
-- =============================================================================


-- =============================================================================
-- PROCEDURE 1: enroll_student
-- Safely enrolls a student in a course.
-- Checks capacity and prevents duplicate enrollments.
-- =============================================================================

CREATE OR REPLACE PROCEDURE enroll_student(
    p_student_id    INT,
    p_course_id     INT
)
LANGUAGE plpgsql
AS 
$$
DECLARE
    v_current_enrollments   INT;
    v_max_students          INT;
    v_existing_enrollment   INT;
BEGIN
    -- Check if student exists
    IF NOT EXISTS (SELECT 1 FROM students WHERE student_id = p_student_id) THEN
        RAISE EXCEPTION 'Student with ID % does not exist.', p_student_id;
    END IF;

    -- Check if course exists
    IF NOT EXISTS (SELECT 1 FROM courses WHERE course_id = p_course_id) THEN
        RAISE EXCEPTION 'Course with ID % does not exist.', p_course_id;
    END IF;

    -- Check if student is already enrolled
    SELECT COUNT(*) INTO v_existing_enrollment
    FROM enrollments
    WHERE student_id = p_student_id
    AND course_id = p_course_id;

    IF v_existing_enrollment > 0 THEN
        RAISE EXCEPTION 'Student % is already enrolled in course %.', 
            p_student_id, p_course_id;
    END IF;

    -- Check course capacity
    SELECT max_students INTO v_max_students
    FROM courses
    WHERE course_id = p_course_id;

    SELECT COUNT(*) INTO v_current_enrollments
    FROM enrollments
    WHERE course_id = p_course_id
    AND status = 'Active';

    IF v_current_enrollments >= v_max_students THEN
        RAISE EXCEPTION 'Course % has reached maximum capacity of % students.',
            p_course_id, v_max_students;
    END IF;

    -- Enroll the student
    INSERT INTO enrollments (student_id, course_id, enrollment_date, status)
    VALUES (p_student_id, p_course_id, CURRENT_DATE, 'Active');

    RAISE NOTICE 'Student % successfully enrolled in course %.', 
        p_student_id, p_course_id;
END;
$$
;


-- =============================================================================
-- PROCEDURE 2: record_grade
-- Records a grade for a specific enrollment.
-- Prevents duplicate grade records.
-- =============================================================================

CREATE OR REPLACE PROCEDURE record_grade(
    p_enrollment_id     INT,
    p_letter_grade      VARCHAR,
    p_percentage_score  NUMERIC,
    p_gpa_value         NUMERIC
)
LANGUAGE plpgsql
AS 
$$
BEGIN
    -- Check if enrollment exists
    IF NOT EXISTS (SELECT 1 FROM enrollments WHERE enrollment_id = p_enrollment_id) THEN
        RAISE EXCEPTION 'Enrollment with ID % does not exist.', p_enrollment_id;
    END IF;

    -- Check if grade already exists for this enrollment
    IF EXISTS (SELECT 1 FROM grades WHERE enrollment_id = p_enrollment_id) THEN
        RAISE EXCEPTION 'A grade already exists for enrollment %.', p_enrollment_id;
    END IF;

    -- Validate percentage score
    IF p_percentage_score < 0 OR p_percentage_score > 100 THEN
        RAISE EXCEPTION 'Percentage score must be between 0 and 100.';
    END IF;

    -- Validate GPA value
    IF p_gpa_value < 0 OR p_gpa_value > 4 THEN
        RAISE EXCEPTION 'GPA value must be between 0 and 4.';
    END IF;

    -- Insert the grade
    INSERT INTO grades (
        enrollment_id, letter_grade, percentage_score,
        gpa_value, date_recorded
    )
    VALUES (
        p_enrollment_id, p_letter_grade, p_percentage_score,
        p_gpa_value, CURRENT_DATE
    );

    RAISE NOTICE 'Grade % recorded for enrollment %.', 
        p_letter_grade, p_enrollment_id;
END;
$$
;


-- =============================================================================
-- PROCEDURE 3: record_attendance
-- Records attendance for a specific enrollment on a specific date.
-- Prevents duplicate attendance records for the same date.
-- =============================================================================

CREATE OR REPLACE PROCEDURE record_attendance(
    p_enrollment_id     INT,
    p_attendance_date   DATE,
    p_status            VARCHAR,
    p_notes             VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql
AS 
$$
BEGIN
    -- Check if enrollment exists
    IF NOT EXISTS (SELECT 1 FROM enrollments WHERE enrollment_id = p_enrollment_id) THEN
        RAISE EXCEPTION 'Enrollment with ID % does not exist.', p_enrollment_id;
    END IF;

    -- Check if attendance already recorded for this date
    IF EXISTS (
        SELECT 1 FROM attendance
        WHERE enrollment_id = p_enrollment_id
        AND attendance_date = p_attendance_date
    ) THEN
        RAISE EXCEPTION 'Attendance already recorded for enrollment % on %.', 
            p_enrollment_id, p_attendance_date;
    END IF;

    -- Validate status
    IF p_status NOT IN ('Present', 'Absent', 'Late', 'Excused') THEN
        RAISE EXCEPTION 'Invalid attendance status: %. Must be Present, Absent, Late or Excused.', 
            p_status;
    END IF;

    -- Insert attendance record
    INSERT INTO attendance (
        enrollment_id, attendance_date, status, notes
    )
    VALUES (
        p_enrollment_id, p_attendance_date, p_status, p_notes
    );

    RAISE NOTICE 'Attendance recorded for enrollment % on %.', 
        p_enrollment_id, p_attendance_date;
END;
$$
;


-- =============================================================================
-- PROCEDURE 4: update_student_status
-- Updates the status of a student record.
-- =============================================================================

CREATE OR REPLACE PROCEDURE update_student_status(
    p_student_id    INT,
    p_new_status    VARCHAR
)
LANGUAGE plpgsql
AS 
$$
BEGIN
    -- Check if student exists
    IF NOT EXISTS (SELECT 1 FROM students WHERE student_id = p_student_id) THEN
        RAISE EXCEPTION 'Student with ID % does not exist.', p_student_id;
    END IF;

    -- Validate new status
    IF p_new_status NOT IN ('Active', 'Inactive', 'Graduated', 'Suspended') THEN
        RAISE EXCEPTION 'Invalid status: %. Must be Active, Inactive, Graduated or Suspended.', 
            p_new_status;
    END IF;

    -- Update the status
    UPDATE students
    SET     status      = p_new_status,
            updated_at  = CURRENT_TIMESTAMP
    WHERE   student_id  = p_student_id;

    RAISE NOTICE 'Student % status updated to %.', p_student_id, p_new_status;
END;
$$
;