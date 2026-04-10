-- =============================================================================
-- STUDENT RECORDS MANAGEMENT SYSTEM
-- Schema: Table Definitions
-- Database: Azure PostgreSQL
-- Standard: Third Normal Form (3NF)
-- =============================================================================


-- =============================================================================
-- TABLE 1: students
-- Stores the personal and academic profile of every registered student.
-- =============================================================================

CREATE TABLE IF NOT EXISTS students (
    student_id      SERIAL          PRIMARY KEY,
    first_name      VARCHAR(50)     NOT NULL,
    last_name       VARCHAR(50)     NOT NULL,
    date_of_birth   DATE            NOT NULL,
    gender          VARCHAR(10)     NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    email           VARCHAR(100)    NOT NULL UNIQUE,
    phone_number    VARCHAR(20),
    program         VARCHAR(100)    NOT NULL,
    year_of_study   SMALLINT        NOT NULL CHECK (year_of_study BETWEEN 1 AND 6),
    status          VARCHAR(20)     NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive', 'Graduated', 'Suspended')),
    enrollment_date DATE            NOT NULL,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- TABLE 2: courses
-- Stores information about every course offered by the university.
-- =============================================================================

CREATE TABLE IF NOT EXISTS courses (
    course_id       SERIAL          PRIMARY KEY,
    course_code     VARCHAR(20)     NOT NULL UNIQUE,
    course_name     VARCHAR(100)    NOT NULL,
    department      VARCHAR(100)    NOT NULL,
    credits         SMALLINT        NOT NULL CHECK (credits BETWEEN 1 AND 8),
    semester        VARCHAR(20)     NOT NULL CHECK (semester IN ('Semester 1', 'Semester 2', 'Full Year')),
    max_students    SMALLINT        NOT NULL CHECK (max_students > 0),
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- TABLE 3: enrollments
-- Records which student is enrolled in which course.
-- Enforces referential integrity through foreign keys.
-- =============================================================================

CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id       SERIAL          PRIMARY KEY,
    student_id          INT             NOT NULL REFERENCES students(student_id) ON DELETE RESTRICT,
    course_id           INT             NOT NULL REFERENCES courses(course_id) ON DELETE RESTRICT,
    enrollment_date     DATE            NOT NULL DEFAULT CURRENT_DATE,
    status              VARCHAR(20)     NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'Withdrawn', 'Completed')),
    created_at          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_student_course UNIQUE (student_id, course_id)
);

-- =============================================================================
-- TABLE 4: grades
-- Records the academic performance of a student for a specific enrollment.
-- =============================================================================

CREATE TABLE IF NOT EXISTS grades (
    grade_id            SERIAL          PRIMARY KEY,
    enrollment_id       INT             NOT NULL REFERENCES enrollments(enrollment_id) ON DELETE RESTRICT,
    letter_grade        VARCHAR(5)      NOT NULL CHECK (letter_grade IN ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F')),
    percentage_score    NUMERIC(5,2)    NOT NULL CHECK (percentage_score BETWEEN 0 AND 100),
    gpa_value           NUMERIC(3,2)    NOT NULL CHECK (gpa_value BETWEEN 0 AND 4),
    date_recorded       DATE            NOT NULL DEFAULT CURRENT_DATE,
    created_at          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_enrollment_grade UNIQUE (enrollment_id)
);

-- =============================================================================
-- TABLE 5: attendance
-- Records student attendance for each session of a specific enrollment.
-- =============================================================================

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id       SERIAL          PRIMARY KEY,
    enrollment_id       INT             NOT NULL REFERENCES enrollments(enrollment_id) ON DELETE RESTRICT,
    attendance_date     DATE            NOT NULL,
    status              VARCHAR(20)     NOT NULL CHECK (status IN ('Present', 'Absent', 'Late', 'Excused')),
    notes               VARCHAR(255),
    created_at          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_enrollment_date UNIQUE (enrollment_id, attendance_date)
);