# =============================================================================
# STUDENT RECORDS MANAGEMENT SYSTEM
# File: etl/extract.py
# Purpose: Extracts data from Azure PostgreSQL for ETL processing.
# =============================================================================

import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# -----------------------------------------------------------------------------
# Load environment variables
# -----------------------------------------------------------------------------
load_dotenv()

# -----------------------------------------------------------------------------
# Database connection configuration
# -----------------------------------------------------------------------------
DB_CONFIG = {
    'host':     os.getenv('DB_HOST'),
    'dbname':   os.getenv('DB_NAME'),
    'user':     os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port':     os.getenv('DB_PORT', '5432')
}


def get_connection():
    """
    Establishes and returns a connection to Azure PostgreSQL.
    """
    return psycopg2.connect(**DB_CONFIG)
# =============================================================================
# SECTION 2: Extract Functions
# =============================================================================

def extract_students():
    """
    Extracts all student records from the database.
    Returns a pandas DataFrame.
    """
    connection = None
    try:
        connection = get_connection()
        query = """
            SELECT
                student_id,
                first_name,
                last_name,
                date_of_birth,
                gender,
                email,
                phone_number,
                program,
                year_of_study,
                status,
                enrollment_date,
                created_at,
                updated_at
            FROM students
            ORDER BY student_id;
        """
        df = pd.read_sql(query, connection)
        print(f"Extracted {len(df)} student records.")
        return df
    except Exception as e:
        print(f"Error extracting students: {e}")
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()


def extract_courses():
    """
    Extracts all course records from the database.
    Returns a pandas DataFrame.
    """
    connection = None
    try:
        connection = get_connection()
        query = """
            SELECT
                course_id,
                course_code,
                course_name,
                department,
                credits,
                semester,
                max_students,
                created_at
            FROM courses
            ORDER BY course_id;
        """
        df = pd.read_sql(query, connection)
        print(f"Extracted {len(df)} course records.")
        return df
    except Exception as e:
        print(f"Error extracting courses: {e}")
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()


def extract_enrollments():
    """
    Extracts all enrollment records with student and course details.
    Returns a pandas DataFrame.
    """
    connection = None
    try:
        connection = get_connection()
        query = """
            SELECT
                e.enrollment_id,
                e.student_id,
                s.first_name,
                s.last_name,
                e.course_id,
                c.course_code,
                c.course_name,
                e.enrollment_date,
                e.status
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            JOIN courses c ON e.course_id = c.course_id
            ORDER BY e.enrollment_id;
        """
        df = pd.read_sql(query, connection)
        print(f"Extracted {len(df)} enrollment records.")
        return df
    except Exception as e:
        print(f"Error extracting enrollments: {e}")
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()


def extract_grades():
    """
    Extracts all grade records with student and course details.
    Returns a pandas DataFrame.
    """
    connection = None
    try:
        connection = get_connection()
        query = """
            SELECT
                g.grade_id,
                g.enrollment_id,
                s.first_name,
                s.last_name,
                c.course_code,
                c.course_name,
                g.letter_grade,
                g.percentage_score,
                g.gpa_value,
                g.date_recorded
            FROM grades g
            JOIN enrollments e ON g.enrollment_id = e.enrollment_id
            JOIN students s ON e.student_id = s.student_id
            JOIN courses c ON e.course_id = c.course_id
            ORDER BY g.grade_id;
        """
        df = pd.read_sql(query, connection)
        print(f"Extracted {len(df)} grade records.")
        return df
    except Exception as e:
        print(f"Error extracting grades: {e}")
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()


def extract_attendance():
    """
    Extracts all attendance records with student and course details.
    Returns a pandas DataFrame.
    """
    connection = None
    try:
        connection = get_connection()
        query = """
            SELECT
                a.attendance_id,
                a.enrollment_id,
                s.first_name,
                s.last_name,
                c.course_code,
                c.course_name,
                a.attendance_date,
                a.status,
                a.notes
            FROM attendance a
            JOIN enrollments e ON a.enrollment_id = e.enrollment_id
            JOIN students s ON e.student_id = s.student_id
            JOIN courses c ON e.course_id = c.course_id
            ORDER BY a.attendance_id;
        """
        df = pd.read_sql(query, connection)
        print(f"Extracted {len(df)} attendance records.")
        return df
    except Exception as e:
        print(f"Error extracting attendance: {e}")
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()


def extract_student_summary():
    """
    Extracts a comprehensive summary of each student including
    enrollment count, average grade and attendance rate.
    Returns a pandas DataFrame.
    """
    connection = None
    try:
        connection = get_connection()
        query = """
            SELECT
                s.student_id,
                s.first_name,
                s.last_name,
                s.program,
                s.year_of_study,
                s.status,
                COUNT(DISTINCT e.enrollment_id)         AS total_enrollments,
                ROUND(AVG(g.percentage_score), 2)       AS average_grade,
                ROUND(AVG(g.gpa_value), 2)              AS average_gpa,
                COUNT(DISTINCT a.attendance_id)         AS total_sessions,
                SUM(CASE WHEN a.status = 'Present' 
                    THEN 1 ELSE 0 END)                  AS sessions_present,
                ROUND(
                    SUM(CASE WHEN a.status = 'Present'
                        THEN 1 ELSE 0 END) * 100.0 /
                    NULLIF(COUNT(DISTINCT a.attendance_id), 0)
                , 2)                                    AS attendance_rate
            FROM students s
            LEFT JOIN enrollments e ON s.student_id = e.student_id
            LEFT JOIN grades g ON e.enrollment_id = g.enrollment_id
            LEFT JOIN attendance a ON e.enrollment_id = a.enrollment_id
            GROUP BY s.student_id, s.first_name, s.last_name,
                     s.program, s.year_of_study, s.status
            ORDER BY s.student_id;
        """
        df = pd.read_sql(query, connection)
        print(f"Extracted {len(df)} student summary records.")
        return df
    except Exception as e:
        print(f"Error extracting student summary: {e}")
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()