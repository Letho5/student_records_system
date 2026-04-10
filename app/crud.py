# =============================================================================
# STUDENT RECORDS MANAGEMENT SYSTEM
# File: app/crud.py
# Purpose: All database operations for the CLI application.
#          Create, Read, Update and Delete functions for all tables.
# =============================================================================

from app.db_connection import get_connection
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# =============================================================================
# SECTION 2: Student Operations
# =============================================================================

def get_all_students():
    """
    Retrieves all students from the database.
    Returns a list of tuples.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                student_id, first_name, last_name,
                program, year_of_study, status, email
            FROM students
            ORDER BY student_id;
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving students: {e}")
        return []
    finally:
        if connection:
            connection.close()


def get_student_by_id(student_id):
    """
    Retrieves a single student record by ID.
    Returns a single tuple or None.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                student_id, first_name, last_name, date_of_birth,
                gender, email, phone_number, program,
                year_of_study, status, enrollment_date
            FROM students
            WHERE student_id = %s;
        """, (student_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error retrieving student: {e}")
        return None
    finally:
        if connection:
            connection.close()


def add_student(first_name, last_name, date_of_birth, gender,
                email, phone_number, program, year_of_study,
                status, enrollment_date):
    """
    Inserts a new student record into the database.
    Returns True if successful, False otherwise.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO students (
                first_name, last_name, date_of_birth, gender,
                email, phone_number, program, year_of_study,
                status, enrollment_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING student_id;
        """, (first_name, last_name, date_of_birth, gender,
              email, phone_number, program, year_of_study,
              status, enrollment_date))
        student_id = cursor.fetchone()[0]
        connection.commit()
        print(f"Student added successfully with ID: {student_id}")
        return True
    except Exception as e:
        print(f"Error adding student: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()


def update_student_status(student_id, new_status):
    """
    Updates the status of a student using the stored procedure.
    Returns True if successful, False otherwise.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "CALL update_student_status(%s, %s);",
            (student_id, new_status)
        )
        connection.commit()
        print(f"Student {student_id} status updated to {new_status}.")
        return True
    except Exception as e:
        print(f"Error updating student status: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()


def delete_student(student_id):
    """
    Deletes a student record from the database.
    Will fail safely if the student has existing enrollments.
    Returns True if successful, False otherwise.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM students WHERE student_id = %s;",
            (student_id,)
        )
        connection.commit()
        print(f"Student {student_id} deleted successfully.")
        return True
    except Exception as e:
        print(f"Error deleting student: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()
# =============================================================================
# SECTION 3: Course Operations
# =============================================================================

def get_all_courses():
    """
    Retrieves all courses from the database.
    Returns a list of tuples.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                course_id, course_code, course_name,
                department, credits, semester, max_students
            FROM courses
            ORDER BY course_id;
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving courses: {e}")
        return []
    finally:
        if connection:
            connection.close()


def get_course_by_id(course_id):
    """
    Retrieves a single course record by ID.
    Returns a single tuple or None.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                course_id, course_code, course_name,
                department, credits, semester, max_students
            FROM courses
            WHERE course_id = %s;
        """, (course_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error retrieving course: {e}")
        return None
    finally:
        if connection:
            connection.close()


def add_course(course_code, course_name, department,
               credits, semester, max_students):
    """
    Inserts a new course record into the database.
    Returns True if successful, False otherwise.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO courses (
                course_code, course_name, department,
                credits, semester, max_students
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING course_id;
        """, (course_code, course_name, department,
              credits, semester, max_students))
        course_id = cursor.fetchone()[0]
        connection.commit()
        print(f"Course added successfully with ID: {course_id}")
        return True
    except Exception as e:
        print(f"Error adding course: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()


def get_course_enrollment_summary():
    """
    Retrieves course enrollment summary from the view.
    Returns a list of tuples.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                course_code, course_name, department,
                semester, max_students,
                current_enrollments, available_spots
            FROM vw_course_enrollment_summary
            ORDER BY course_code;
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving course summary: {e}")
        return []
    finally:
        if connection:
            connection.close()

# =============================================================================
# SECTION 4: Enrollment Operations
# =============================================================================

def get_all_enrollments():
    """
    Retrieves all enrollments with student and course details.
    Returns a list of tuples.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                enrollment_id, student_id, full_name,
                course_code, course_name,
                enrollment_date, status
            FROM vw_student_grades
            ORDER BY enrollment_id;
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving enrollments: {e}")
        return []
    finally:
        if connection:
            connection.close()


def get_enrollments_by_student(student_id):
    """
    Retrieves all enrollments for a specific student.
    Returns a list of tuples.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                e.enrollment_id,
                c.course_code,
                c.course_name,
                e.enrollment_date,
                e.status
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.student_id = %s
            ORDER BY e.enrollment_date;
        """, (student_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving student enrollments: {e}")
        return []
    finally:
        if connection:
            connection.close()


def enroll_student(student_id, course_id):
    """
    Enrolls a student in a course using the stored procedure.
    Returns True if successful, False otherwise.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "CALL enroll_student(%s, %s);",
            (student_id, course_id)
        )
        connection.commit()
        print(f"Student {student_id} enrolled in course {course_id} successfully.")
        return True
    except Exception as e:
        print(f"Error enrolling student: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()


def withdraw_student(enrollment_id):
    """
    Withdraws a student from an enrollment by updating status.
    Returns True if successful, False otherwise.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE enrollments
            SET status = 'Withdrawn'
            WHERE enrollment_id = %s;
        """, (enrollment_id,))
        connection.commit()
        print(f"Enrollment {enrollment_id} withdrawn successfully.")
        return True
    except Exception as e:
        print(f"Error withdrawing enrollment: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()
# =============================================================================
# SECTION 5: Grades Operations
# =============================================================================

def get_grades_by_student(student_id):
    """
    Retrieves all grades for a specific student.
    Returns a list of tuples.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                g.grade_id,
                c.course_code,
                c.course_name,
                g.letter_grade,
                g.percentage_score,
                g.gpa_value,
                g.date_recorded
            FROM grades g
            JOIN enrollments e ON g.enrollment_id = e.enrollment_id
            JOIN courses c     ON e.course_id     = c.course_id
            WHERE e.student_id = %s
            ORDER BY g.date_recorded;
        """, (student_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving grades: {e}")
        return []
    finally:
        if connection:
            connection.close()


def record_grade(enrollment_id, letter_grade,
                 percentage_score, gpa_value):
    """
    Records a grade for a specific enrollment
    using the stored procedure.
    Returns True if successful, False otherwise.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "CALL record_grade(%s, %s, %s, %s);",
            (enrollment_id, letter_grade,
             percentage_score, gpa_value)
        )
        connection.commit()
        print(f"Grade {letter_grade} recorded for enrollment {enrollment_id}.")
        return True
    except Exception as e:
        print(f"Error recording grade: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()


def get_failing_students():
    """
    Retrieves all failing students from the view.
    Returns a list of tuples.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                student_id, full_name, program,
                year_of_study, average_grade,
                average_gpa, attendance_rate
            FROM vw_failing_students;
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving failing students: {e}")
        return []
    finally:
        if connection:
            connection.close()


def get_top_performing_students():
    """
    Retrieves all top performing students from the view.
    Returns a list of tuples.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                student_id, full_name, program,
                year_of_study, average_grade,
                average_gpa, attendance_rate
            FROM vw_top_performing_students;
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving top students: {e}")
        return []
    finally:
        if connection:
            connection.close()


# =============================================================================
# SECTION 6: Attendance Operations
# =============================================================================

def get_attendance_by_student(student_id):
    """
    Retrieves attendance summary for a specific student.
    Returns a list of tuples.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                course_code,
                course_name,
                total_sessions,
                sessions_present,
                sessions_absent,
                attendance_rate,
                attendance_standing
            FROM vw_attendance_summary
            WHERE student_id = %s
            ORDER BY course_code;
        """, (student_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving attendance: {e}")
        return []
    finally:
        if connection:
            connection.close()


def record_attendance(enrollment_id, attendance_date,
                      status, notes=None):
    """
    Records attendance for a specific enrollment
    using the stored procedure.
    Returns True if successful, False otherwise.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "CALL record_attendance(%s, %s, %s, %s);",
            (enrollment_id, attendance_date, status, notes)
        )
        connection.commit()
        print(f"Attendance recorded for enrollment {enrollment_id}.")
        return True
    except Exception as e:
        print(f"Error recording attendance: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()


def get_attendance_summary():
    """
    Retrieves full attendance summary from the view.
    Returns a list of tuples.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                full_name,
                course_code,
                course_name,
                total_sessions,
                sessions_present,
                attendance_rate,
                attendance_standing
            FROM vw_attendance_summary
            ORDER BY attendance_rate ASC;
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving attendance summary: {e}")
        return []
    finally:
        if connection:
            connection.close()