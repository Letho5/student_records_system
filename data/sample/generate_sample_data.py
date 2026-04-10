# =============================================================================
# STUDENT RECORDS MANAGEMENT SYSTEM
# File: data/sample/generate_sample_data.py
# Purpose: Generates realistic sample data and loads it into Azure PostgreSQL.
# =============================================================================

import psycopg2
import random
from faker import Faker
from dotenv import load_dotenv
import os
from datetime import date, timedelta

# -----------------------------------------------------------------------------
# Initialise Faker and load environment variables
# -----------------------------------------------------------------------------
fake = Faker('en_US')
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

# -----------------------------------------------------------------------------
# Data generation configuration
# -----------------------------------------------------------------------------
NUM_STUDENTS    = 500
NUM_COURSES     = 25
NUM_ENROLLMENTS = 1250

# =============================================================================
# SECTION 2: Data Generation Functions
# =============================================================================

# -----------------------------------------------------------------------------
# Generate Students
# -----------------------------------------------------------------------------
def generate_students(num_students):
    """Generates a list of realistic student records."""

    programs = [
        'Computer Science', 'Information Technology', 'Business Administration',
        'Accounting', 'Human Resources', 'Marketing', 'Civil Engineering',
        'Mechanical Engineering', 'Electrical Engineering', 'Data Science',
        'Psychology', 'Public Administration', 'Law', 'Medicine', 'Nursing'
    ]

    genders = ['Male', 'Female', 'Other']
    statuses = ['Active', 'Active', 'Active', 'Active', 'Inactive', 'Graduated', 'Suspended']

    students = []
    emails_used = set()

    for _ in range(num_students):
        gender = random.choice(genders)

        if gender == 'Male':
            first_name = fake.first_name_male()
        elif gender == 'Female':
            first_name = fake.first_name_female()
        else:
            first_name = fake.first_name()

        last_name = fake.last_name()

        # Generate a unique email address
        base_email = f"{first_name.lower()}.{last_name.lower()}@university.ac.za"
        email = base_email
        counter = 1
        while email in emails_used:
            email = f"{first_name.lower()}.{last_name.lower()}{counter}@university.ac.za"
            counter += 1
        emails_used.add(email)

        dob = fake.date_of_birth(minimum_age=17, maximum_age=35)
        enrollment_date = fake.date_between(start_date=date(2020, 1, 1), end_date=date.today())

        students.append((
            first_name,
            last_name,
            dob,
            gender,
            email,
            fake.phone_number()[:20],
            random.choice(programs),
            random.randint(1, 4),
            random.choice(statuses),
            enrollment_date
        ))

    return students


# -----------------------------------------------------------------------------
# Generate Courses
# -----------------------------------------------------------------------------
def generate_courses(num_courses):
    """Generates a list of realistic university course records."""

    course_data = [
        ('CS101', 'Introduction to Programming', 'Computer Science', 3, 'Semester 1'),
        ('CS201', 'Data Structures and Algorithms', 'Computer Science', 4, 'Semester 2'),
        ('CS301', 'Database Systems', 'Computer Science', 4, 'Semester 1'),
        ('CS401', 'Software Engineering', 'Computer Science', 4, 'Semester 2'),
        ('IT101', 'Networking Fundamentals', 'Information Technology', 3, 'Semester 1'),
        ('IT201', 'Cybersecurity Essentials', 'Information Technology', 3, 'Semester 2'),
        ('IT301', 'Cloud Computing', 'Information Technology', 4, 'Semester 1'),
        ('DS101', 'Introduction to Data Science', 'Data Science', 3, 'Semester 1'),
        ('DS201', 'Machine Learning Fundamentals', 'Data Science', 4, 'Semester 2'),
        ('DS301', 'Big Data Analytics', 'Data Science', 4, 'Full Year'),
        ('BUS101', 'Business Management', 'Business Administration', 3, 'Semester 1'),
        ('BUS201', 'Strategic Management', 'Business Administration', 4, 'Semester 2'),
        ('ACC101', 'Financial Accounting', 'Accounting', 3, 'Semester 1'),
        ('ACC201', 'Management Accounting', 'Accounting', 4, 'Semester 2'),
        ('MKT101', 'Marketing Principles', 'Marketing', 3, 'Semester 1'),
        ('MKT201', 'Digital Marketing', 'Marketing', 3, 'Semester 2'),
        ('HR101', 'Human Resources Management', 'Human Resources', 3, 'Semester 1'),
        ('HR201', 'Labour Relations', 'Human Resources', 3, 'Semester 2'),
        ('LAW101', 'Introduction to Law', 'Law', 4, 'Semester 1'),
        ('LAW201', 'Commercial Law', 'Law', 4, 'Semester 2'),
        ('ENG101', 'Engineering Mathematics', 'Engineering', 4, 'Semester 1'),
        ('ENG201', 'Thermodynamics', 'Mechanical Engineering', 4, 'Semester 2'),
        ('PSY101', 'Introduction to Psychology', 'Psychology', 3, 'Semester 1'),
        ('PUB101', 'Public Administration Fundamentals', 'Public Administration', 3, 'Semester 1'),
        ('NUR101', 'Foundations of Nursing', 'Nursing', 4, 'Semester 1'),
    ]

    courses = []
    for code, name, department, credits, semester in course_data[:num_courses]:
        courses.append((
            code,
            name,
            department,
            credits,
            semester,
            random.randint(30, 60)
        ))

    return courses


# -----------------------------------------------------------------------------
# Generate Enrollments
# -----------------------------------------------------------------------------
def generate_enrollments(student_ids, course_ids, num_enrollments):
    """Generates enrollment records linking students to courses."""

    enrollments = []
    combinations_used = set()
    statuses = ['Active', 'Active', 'Active', 'Completed', 'Withdrawn']
    attempts = 0
    max_attempts = num_enrollments * 10

    while len(enrollments) < num_enrollments and attempts < max_attempts:
        student_id = random.choice(student_ids)
        course_id = random.choice(course_ids)
        combo = (student_id, course_id)
        attempts += 1

        if combo not in combinations_used:
            combinations_used.add(combo)
            enrollment_date = fake.date_between(
                start_date=date(2020, 1, 1),
                end_date=date.today()
            )
            enrollments.append((
                student_id,
                course_id,
                enrollment_date,
                random.choice(statuses)
            ))

    return enrollments


# -----------------------------------------------------------------------------
# Generate Grades
# -----------------------------------------------------------------------------
def generate_grades(enrollment_ids):
    """Generates grade records for each enrollment."""

    grade_map = [
        ('A',  95.0, 4.0), ('A',  92.0, 4.0), ('A-', 88.0, 3.7),
        ('B+', 85.0, 3.3), ('B',  82.0, 3.0), ('B-', 78.0, 2.7),
        ('C+', 75.0, 2.3), ('C',  72.0, 2.0), ('C-', 68.0, 1.7),
        ('D',  60.0, 1.0), ('F',  45.0, 0.0), ('F',  30.0, 0.0),
    ]

    grades = []
    for enrollment_id in enrollment_ids:
        letter, percentage, gpa = random.choice(grade_map)
        percentage += round(random.uniform(-2.0, 2.0), 2)
        percentage = max(0.0, min(100.0, percentage))
        grades.append((
            enrollment_id,
            letter,
            round(percentage, 2),
            gpa,
            fake.date_between(start_date=date(2020, 6, 1), end_date=date.today())
        ))

    return grades


# -----------------------------------------------------------------------------
# Generate Attendance
# -----------------------------------------------------------------------------
def generate_attendance(enrollment_ids):
    """Generates attendance records for each enrollment."""

    statuses = ['Present', 'Present', 'Present', 'Present', 'Absent', 'Late', 'Excused']
    attendance = []
    dates_used = {}

    for enrollment_id in enrollment_ids:
        dates_used[enrollment_id] = set()
        num_sessions = random.randint(20, 30)
        sessions_added = 0
        attempts = 0

        while sessions_added < num_sessions and attempts < num_sessions * 5:
            session_date = fake.date_between(
                start_date=date(2020, 1, 1),
                end_date=date.today()
            )
            attempts += 1

            if session_date not in dates_used[enrollment_id]:
                dates_used[enrollment_id].add(session_date)
                status = random.choice(statuses)
                note = None
                if status == 'Absent':
                    note = random.choice([
                        'No reason provided',
                        'Medical appointment',
                        'Family emergency',
                        None
                    ])
                attendance.append((
                    enrollment_id,
                    session_date,
                    status,
                    note
                ))
                sessions_added += 1

    return attendance

# =============================================================================
# SECTION 3: Database Loading Function
# =============================================================================

def load_data():
    """
    Connects to Azure PostgreSQL and loads all generated
    sample data into the database in the correct order.
    """
    connection = None

    try:
        # ---------------------------------------------------------------------
        # Establish connection
        # ---------------------------------------------------------------------
        print("=" * 60)
        print("STUDENT RECORDS SYSTEM — Sample Data Generator")
        print("=" * 60)
        print("\nConnecting to Azure PostgreSQL...")
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        print("Connection successful.\n")

        # ---------------------------------------------------------------------
        # Clear existing data in correct order
        # ---------------------------------------------------------------------
        print("Clearing existing sample data...")
        cursor.execute("TRUNCATE TABLE attendance, grades, enrollments, students, courses RESTART IDENTITY CASCADE;")
        connection.commit()
        print("Existing data cleared.\n")

        # ---------------------------------------------------------------------
        # Load Students
        # ---------------------------------------------------------------------
        print(f"Generating {NUM_STUDENTS} students...")
        students = generate_students(NUM_STUDENTS)
        cursor.executemany("""
            INSERT INTO students (
                first_name, last_name, date_of_birth, gender,
                email, phone_number, program, year_of_study,
                status, enrollment_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, students)
        connection.commit()
        print(f"{NUM_STUDENTS} students loaded successfully.\n")

        # ---------------------------------------------------------------------
        # Load Courses
        # ---------------------------------------------------------------------
        print(f"Generating {NUM_COURSES} courses...")
        courses = generate_courses(NUM_COURSES)
        cursor.executemany("""
            INSERT INTO courses (
                course_code, course_name, department,
                credits, semester, max_students
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, courses)
        connection.commit()
        print(f"{NUM_COURSES} courses loaded successfully.\n")

        # ---------------------------------------------------------------------
        # Retrieve generated IDs for students and courses
        # ---------------------------------------------------------------------
        cursor.execute("SELECT student_id FROM students;")
        student_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT course_id FROM courses;")
        course_ids = [row[0] for row in cursor.fetchall()]

        # ---------------------------------------------------------------------
        # Load Enrollments
        # ---------------------------------------------------------------------
        print(f"Generating {NUM_ENROLLMENTS} enrollments...")
        enrollments = generate_enrollments(student_ids, course_ids, NUM_ENROLLMENTS)
        cursor.executemany("""
            INSERT INTO enrollments (
                student_id, course_id, enrollment_date, status
            ) VALUES (%s, %s, %s, %s)
        """, enrollments)
        connection.commit()
        print(f"{len(enrollments)} enrollments loaded successfully.\n")

        # ---------------------------------------------------------------------
        # Retrieve enrollment IDs
        # ---------------------------------------------------------------------
        cursor.execute("SELECT enrollment_id FROM enrollments;")
        enrollment_ids = [row[0] for row in cursor.fetchall()]

        # ---------------------------------------------------------------------
        # Load Grades
        # ---------------------------------------------------------------------
        print(f"Generating grades for {len(enrollment_ids)} enrollments...")
        grades = generate_grades(enrollment_ids)
        cursor.executemany("""
            INSERT INTO grades (
                enrollment_id, letter_grade, percentage_score,
                gpa_value, date_recorded
            ) VALUES (%s, %s, %s, %s, %s)
        """, grades)
        connection.commit()
        print(f"{len(grades)} grade records loaded successfully.\n")

        # ---------------------------------------------------------------------
        # Load Attendance
        # ---------------------------------------------------------------------
        print(f"Generating attendance records...")
        attendance = generate_attendance(enrollment_ids)
        cursor.executemany("""
            INSERT INTO attendance (
                enrollment_id, attendance_date, status, notes
            ) VALUES (%s, %s, %s, %s)
        """, attendance)
        connection.commit()
        print(f"{len(attendance)} attendance records loaded successfully.\n")

        # ---------------------------------------------------------------------
        # Final summary
        # ---------------------------------------------------------------------
        print("=" * 60)
        print("SAMPLE DATA GENERATION COMPLETE")
        print("=" * 60)
        cursor.execute("SELECT COUNT(*) FROM students;")
        print(f"  Students:   {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM courses;")
        print(f"  Courses:    {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM enrollments;")
        print(f"  Enrollments:{cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM grades;")
        print(f"  Grades:     {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM attendance;")
        print(f"  Attendance: {cursor.fetchone()[0]}")
        print("=" * 60)

    except Exception as e:
        print(f"\nError: {e}")
        if connection:
            connection.rollback()

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\nDatabase connection closed.")


# =============================================================================
# SECTION 4: Entry Point
# =============================================================================
if __name__ == '__main__':
    load_data()