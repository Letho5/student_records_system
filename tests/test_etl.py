# =============================================================================
# STUDENT RECORDS MANAGEMENT SYSTEM
# File: tests/test_etl.py
# Purpose: Automated tests for data quality, ETL pipeline and database integrity.
# =============================================================================

import sys
import os
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
from dotenv import load_dotenv
load_dotenv()

# -----------------------------------------------------------------------------
# Database connection configuration
# -----------------------------------------------------------------------------
DB_CONFIG = {
    'host':     os.getenv('DB_HOST'),
    'dbname':   os.getenv('DB_NAME'),
    'user':     os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port':     os.getenv('DB_PORT', '5432'),
    'sslmode':  'require'
}

# -----------------------------------------------------------------------------
# Test tracking
# -----------------------------------------------------------------------------
tests_passed = 0
tests_failed = 0


def get_connection():
    """Returns a database connection."""
    return psycopg2.connect(**DB_CONFIG)


def test_pass(test_name):
    """Records a passed test."""
    global tests_passed
    tests_passed += 1
    print(f"  PASS  {test_name}")


def test_fail(test_name, reason):
    """Records a failed test."""
    global tests_failed
    tests_failed += 1
    print(f"  FAIL  {test_name} — {reason}")
# =============================================================================
# SECTION 2: Test Functions
# =============================================================================

def test_database_connection():
    """Tests that the database connection is successful."""
    try:
        connection = get_connection()
        connection.close()
        test_pass("Database connection")
    except Exception as e:
        test_fail("Database connection", str(e))


def test_tables_exist():
    """Tests that all five required tables exist in the database."""
    required_tables = [
        'students', 'courses', 'enrollments',
        'grades', 'attendance'
    ]
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        existing_tables = [row[0] for row in cursor.fetchall()]

        for table in required_tables:
            if table in existing_tables:
                test_pass(f"Table exists: {table}")
            else:
                test_fail(f"Table exists: {table}", "Table not found")

    except Exception as e:
        test_fail("Tables exist check", str(e))
    finally:
        if connection:
            connection.close()


def test_data_presence():
    """Tests that each table contains data."""
    tables = [
        'students', 'courses', 'enrollments',
        'grades', 'attendance'
    ]
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            if count > 0:
                test_pass(f"Data present in {table}: {count} records")
            else:
                test_fail(f"Data present in {table}", "Table is empty")

    except Exception as e:
        test_fail("Data presence check", str(e))
    finally:
        if connection:
            connection.close()


def test_no_duplicate_students():
    """Tests that no duplicate email addresses exist in students table."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT email, COUNT(*)
            FROM students
            GROUP BY email
            HAVING COUNT(*) > 1;
        """)
        duplicates = cursor.fetchall()
        if not duplicates:
            test_pass("No duplicate student emails")
        else:
            test_fail(
                "No duplicate student emails",
                f"{len(duplicates)} duplicate emails found"
            )
    except Exception as e:
        test_fail("Duplicate student check", str(e))
    finally:
        if connection:
            connection.close()


def test_no_duplicate_enrollments():
    """Tests that no student is enrolled in the same course twice."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT student_id, course_id, COUNT(*)
            FROM enrollments
            GROUP BY student_id, course_id
            HAVING COUNT(*) > 1;
        """)
        duplicates = cursor.fetchall()
        if not duplicates:
            test_pass("No duplicate enrollments")
        else:
            test_fail(
                "No duplicate enrollments",
                f"{len(duplicates)} duplicate enrollments found"
            )
    except Exception as e:
        test_fail("Duplicate enrollment check", str(e))
    finally:
        if connection:
            connection.close()


def test_grade_score_range():
    """Tests that all percentage scores are between 0 and 100."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM grades
            WHERE percentage_score < 0
            OR percentage_score > 100;
        """)
        invalid = cursor.fetchone()[0]
        if invalid == 0:
            test_pass("All grade scores within valid range")
        else:
            test_fail(
                "Grade score range",
                f"{invalid} scores outside 0-100 range"
            )
    except Exception as e:
        test_fail("Grade score range check", str(e))
    finally:
        if connection:
            connection.close()


def test_gpa_range():
    """Tests that all GPA values are between 0 and 4."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM grades
            WHERE gpa_value < 0
            OR gpa_value > 4;
        """)
        invalid = cursor.fetchone()[0]
        if invalid == 0:
            test_pass("All GPA values within valid range")
        else:
            test_fail(
                "GPA range",
                f"{invalid} GPA values outside 0-4 range"
            )
    except Exception as e:
        test_fail("GPA range check", str(e))
    finally:
        if connection:
            connection.close()


def test_foreign_key_integrity():
    """Tests that all enrollments reference valid students and courses."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Check enrollments reference valid students
        cursor.execute("""
            SELECT COUNT(*)
            FROM enrollments e
            LEFT JOIN students s ON e.student_id = s.student_id
            WHERE s.student_id IS NULL;
        """)
        orphaned_students = cursor.fetchone()[0]

        # Check enrollments reference valid courses
        cursor.execute("""
            SELECT COUNT(*)
            FROM enrollments e
            LEFT JOIN courses c ON e.course_id = c.course_id
            WHERE c.course_id IS NULL;
        """)
        orphaned_courses = cursor.fetchone()[0]

        if orphaned_students == 0:
            test_pass("All enrollments reference valid students")
        else:
            test_fail(
                "Enrollment student references",
                f"{orphaned_students} invalid student references"
            )

        if orphaned_courses == 0:
            test_pass("All enrollments reference valid courses")
        else:
            test_fail(
                "Enrollment course references",
                f"{orphaned_courses} invalid course references"
            )

    except Exception as e:
        test_fail("Foreign key integrity check", str(e))
    finally:
        if connection:
            connection.close()


def test_views_exist():
    """Tests that all six views exist and return data."""
    required_views = [
        'vw_student_overview',
        'vw_course_enrollment_summary',
        'vw_student_grades',
        'vw_attendance_summary',
        'vw_failing_students',
        'vw_top_performing_students'
    ]
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        for view in required_views:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {view};")
                count = cursor.fetchone()[0]
                test_pass(f"View accessible: {view} ({count} records)")
            except Exception:
                test_fail(f"View accessible: {view}", "View not found or error")

    except Exception as e:
        test_fail("Views check", str(e))
    finally:
        if connection:
            connection.close()


def test_etl_extract():
    """Tests that ETL extract functions return data."""
    try:
        from etl.extract import (
            extract_students,
            extract_courses,
            extract_enrollments,
            extract_grades,
            extract_attendance
        )

        datasets = {
            'students':    extract_students(),
            'courses':     extract_courses(),
            'enrollments': extract_enrollments(),
            'grades':      extract_grades(),
            'attendance':  extract_attendance()
        }

        for name, df in datasets.items():
            if not df.empty:
                test_pass(f"ETL extract: {name} ({len(df)} records)")
            else:
                test_fail(f"ETL extract: {name}", "Empty DataFrame returned")

    except Exception as e:
        test_fail("ETL extract", str(e))


def test_etl_transform():
    """Tests that ETL transform functions enrich data correctly."""
    try:
        from etl.extract import extract_students, extract_courses
        from etl.transform import transform_students, transform_courses

        students_df = transform_students(extract_students())
        courses_df  = transform_courses(extract_courses())

        # Check full_name column was created
        if 'full_name' in students_df.columns:
            test_pass("Transform: full_name column created")
        else:
            test_fail("Transform: full_name column", "Column not found")

        # Check age column was created
        if 'age' in students_df.columns:
            test_pass("Transform: age column calculated")
        else:
            test_fail("Transform: age column", "Column not found")

        # Check credit_level column was created
        if 'credit_level' in courses_df.columns:
            test_pass("Transform: credit_level column created")
        else:
            test_fail("Transform: credit_level column", "Column not found")

    except Exception as e:
        test_fail("ETL transform", str(e))


def test_student_status_values():
    """Tests that all student status values are valid."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM students
            WHERE status NOT IN (
                'Active', 'Inactive', 'Graduated', 'Suspended'
            );
        """)
        invalid = cursor.fetchone()[0]
        if invalid == 0:
            test_pass("All student status values are valid")
        else:
            test_fail(
                "Student status values",
                f"{invalid} invalid status values found"
            )
    except Exception as e:
        test_fail("Student status check", str(e))
    finally:
        if connection:
            connection.close()


# =============================================================================
# SECTION 3: Test Runner
# =============================================================================

def run_all_tests():
    """
    Runs all tests in sequence and prints a summary report.
    """
    print("\n" + "=" * 60)
    print("  STUDENT RECORDS SYSTEM — Data Quality Test Suite")
    print("=" * 60)

    print("\n[ DATABASE INTEGRITY ]")
    test_database_connection()
    test_tables_exist()
    test_data_presence()

    print("\n[ DATA QUALITY ]")
    test_no_duplicate_students()
    test_no_duplicate_enrollments()
    test_grade_score_range()
    test_gpa_range()
    test_student_status_values()

    print("\n[ REFERENTIAL INTEGRITY ]")
    test_foreign_key_integrity()

    print("\n[ VIEWS ]")
    test_views_exist()

    print("\n[ ETL PIPELINE ]")
    test_etl_extract()
    test_etl_transform()

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    total = tests_passed + tests_failed
    print("\n" + "=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    print(f"  Total Tests:  {total}")
    print(f"  Passed:       {tests_passed}")
    print(f"  Failed:       {tests_failed}")
    print("=" * 60)

    if tests_failed == 0:
        print("  ALL TESTS PASSED — System is healthy.")
    else:
        print(f"  {tests_failed} TEST(S) FAILED — Review output above.")
    print("=" * 60 + "\n")


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == '__main__':
    run_all_tests()