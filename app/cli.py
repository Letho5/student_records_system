# =============================================================================
# STUDENT RECORDS MANAGEMENT SYSTEM
# File: app/cli.py
# Purpose: Command line interface for the student records system.
# =============================================================================

import os
import sys
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

from app.db_connection import test_connection
from app.crud import (
    get_all_students, get_student_by_id, add_student,
    update_student_status, delete_student,
    get_all_courses, get_course_by_id, add_course,
    get_course_enrollment_summary,
    get_enrollments_by_student, enroll_student, withdraw_student,
    get_grades_by_student, record_grade,
    get_failing_students, get_top_performing_students,
    get_attendance_by_student, record_attendance,
    get_attendance_summary
)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Prints a consistent section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_row(data, widths):
    """Prints a formatted table row."""
    row = ""
    for i, item in enumerate(data):
        row += str(item)[:widths[i]].ljust(widths[i]) + "  "
    print(row)


def get_valid_input(prompt, valid_options=None, input_type=str):
    """
    Prompts the user for input and validates it.
    Repeats until valid input is received.
    """
    while True:
        try:
            value = input_type(input(prompt))
            if valid_options and value not in valid_options:
                print(f"Invalid option. Choose from: {valid_options}")
                continue
            return value
        except ValueError:
            print("Invalid input. Please try again.")
        except KeyboardInterrupt:
            print("\nReturning to menu...")
            return None


def press_enter_to_continue():
    """Pauses execution until the user presses Enter."""
    input("\nPress Enter to continue...")


# =============================================================================
# SECTION 1: Student Management
# =============================================================================

def student_menu():
    """Student management sub-menu."""
    while True:
        print_header("STUDENT MANAGEMENT")
        print("  1. View All Students")
        print("  2. View Student by ID")
        print("  3. Add New Student")
        print("  4. Update Student Status")
        print("  5. Delete Student")
        print("  0. Back to Main Menu")
        print("=" * 60)

        choice = input("  Select option: ").strip()

        if choice == '1':
            view_all_students()
        elif choice == '2':
            view_student_by_id()
        elif choice == '3':
            add_new_student()
        elif choice == '4':
            change_student_status()
        elif choice == '5':
            remove_student()
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def view_all_students():
    """Displays all students in a formatted table."""
    print_header("ALL STUDENTS")
    students = get_all_students()

    if not students:
        print("No students found.")
        press_enter_to_continue()
        return

    widths = [6, 15, 15, 25, 6, 12, 30]
    headers = ['ID', 'First Name', 'Last Name',
               'Program', 'Year', 'Status', 'Email']
    print_row(headers, widths)
    print("-" * 60)

    for student in students:
        print_row(student, widths)

    print(f"\nTotal students: {len(students)}")
    press_enter_to_continue()


def view_student_by_id():
    """Displays a single student record by ID."""
    print_header("VIEW STUDENT BY ID")

    student_id = get_valid_input("  Enter Student ID: ", input_type=int)
    if student_id is None:
        return

    student = get_student_by_id(student_id)

    if not student:
        print(f"No student found with ID {student_id}.")
        press_enter_to_continue()
        return

    print_header(f"STUDENT RECORD — ID {student_id}")
    labels = [
        'Student ID', 'First Name', 'Last Name', 'Date of Birth',
        'Gender', 'Email', 'Phone Number', 'Program',
        'Year of Study', 'Status', 'Enrollment Date'
    ]
    for label, value in zip(labels, student):
        print(f"  {label:<20}: {value}")

    press_enter_to_continue()


def add_new_student():
    """Collects input and adds a new student record."""
    print_header("ADD NEW STUDENT")

    try:
        first_name      = input("  First Name: ").strip()
        last_name       = input("  Last Name: ").strip()
        date_of_birth   = input("  Date of Birth (YYYY-MM-DD): ").strip()
        gender          = get_valid_input(
                            "  Gender (Male/Female/Other): ",
                            valid_options=['Male', 'Female', 'Other']
                          )
        email           = input("  Email: ").strip()
        phone_number    = input("  Phone Number: ").strip()
        program         = input("  Program: ").strip()
        year_of_study   = get_valid_input(
                            "  Year of Study (1-4): ",
                            input_type=int
                          )
        status          = get_valid_input(
                            "  Status (Active/Inactive/Graduated/Suspended): ",
                            valid_options=['Active', 'Inactive',
                                          'Graduated', 'Suspended']
                          )
        enrollment_date = input("  Enrollment Date (YYYY-MM-DD): ").strip()

        add_student(
            first_name, last_name, date_of_birth, gender,
            email, phone_number, program, year_of_study,
            status, enrollment_date
        )

    except KeyboardInterrupt:
        print("\nOperation cancelled.")

    press_enter_to_continue()


def change_student_status():
    """Updates a student's status."""
    print_header("UPDATE STUDENT STATUS")

    student_id = get_valid_input("  Enter Student ID: ", input_type=int)
    if student_id is None:
        return

    new_status = get_valid_input(
        "  New Status (Active/Inactive/Graduated/Suspended): ",
        valid_options=['Active', 'Inactive', 'Graduated', 'Suspended']
    )
    if new_status is None:
        return

    update_student_status(student_id, new_status)
    press_enter_to_continue()


def remove_student():
    """Deletes a student record after confirmation."""
    print_header("DELETE STUDENT")

    student_id = get_valid_input("  Enter Student ID: ", input_type=int)
    if student_id is None:
        return

    student = get_student_by_id(student_id)
    if not student:
        print(f"No student found with ID {student_id}.")
        press_enter_to_continue()
        return

    confirm = input(
        f"  Delete student '{student[1]} {student[2]}'? (yes/no): "
    ).strip().lower()

    if confirm == 'yes':
        delete_student(student_id)
    else:
        print("  Deletion cancelled.")

    press_enter_to_continue()


# =============================================================================
# SECTION 2: Course Management
# =============================================================================

def course_menu():
    """Course management sub-menu."""
    while True:
        print_header("COURSE MANAGEMENT")
        print("  1. View All Courses")
        print("  2. View Course by ID")
        print("  3. Add New Course")
        print("  4. View Enrollment Summary")
        print("  0. Back to Main Menu")
        print("=" * 60)

        choice = input("  Select option: ").strip()

        if choice == '1':
            view_all_courses()
        elif choice == '2':
            view_course_by_id()
        elif choice == '3':
            add_new_course()
        elif choice == '4':
            view_course_enrollment_summary()
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def view_all_courses():
    """Displays all courses in a formatted table."""
    print_header("ALL COURSES")
    courses = get_all_courses()

    if not courses:
        print("No courses found.")
        press_enter_to_continue()
        return

    widths = [6, 10, 30, 25, 8, 12, 8]
    headers = ['ID', 'Code', 'Course Name',
               'Department', 'Credits', 'Semester', 'Max']
    print_row(headers, widths)
    print("-" * 60)

    for course in courses:
        print_row(course, widths)

    print(f"\nTotal courses: {len(courses)}")
    press_enter_to_continue()


def view_course_by_id():
    """Displays a single course record by ID."""
    print_header("VIEW COURSE BY ID")

    course_id = get_valid_input("  Enter Course ID: ", input_type=int)
    if course_id is None:
        return

    course = get_course_by_id(course_id)

    if not course:
        print(f"No course found with ID {course_id}.")
        press_enter_to_continue()
        return

    print_header(f"COURSE RECORD — ID {course_id}")
    labels = [
        'Course ID', 'Course Code', 'Course Name',
        'Department', 'Credits', 'Semester', 'Max Students'
    ]
    for label, value in zip(labels, course):
        print(f"  {label:<20}: {value}")

    press_enter_to_continue()


def add_new_course():
    """Collects input and adds a new course record."""
    print_header("ADD NEW COURSE")

    try:
        course_code  = input("  Course Code: ").strip().upper()
        course_name  = input("  Course Name: ").strip()
        department   = input("  Department: ").strip()
        credits      = get_valid_input(
                         "  Credits (1-8): ",
                         input_type=int
                       )
        semester     = get_valid_input(
                         "  Semester (Semester 1/Semester 2/Full Year): ",
                         valid_options=['Semester 1', 'Semester 2', 'Full Year']
                       )
        max_students = get_valid_input(
                         "  Max Students: ",
                         input_type=int
                       )

        add_course(
            course_code, course_name, department,
            credits, semester, max_students
        )

    except KeyboardInterrupt:
        print("\nOperation cancelled.")

    press_enter_to_continue()


def view_course_enrollment_summary():
    """Displays enrollment summary for all courses."""
    print_header("COURSE ENROLLMENT SUMMARY")
    courses = get_course_enrollment_summary()

    if not courses:
        print("No course data found.")
        press_enter_to_continue()
        return

    widths = [10, 25, 20, 12, 8, 12, 10]
    headers = ['Code', 'Course Name', 'Department',
               'Semester', 'Max', 'Enrolled', 'Available']
    print_row(headers, widths)
    print("-" * 60)

    for course in courses:
        print_row(course, widths)

    press_enter_to_continue()


# =============================================================================
# SECTION 3: Enrollment Management
# =============================================================================

def enrollment_menu():
    """Enrollment management sub-menu."""
    while True:
        print_header("ENROLLMENT MANAGEMENT")
        print("  1. View Student Enrollments")
        print("  2. Enroll Student in Course")
        print("  3. Withdraw Student from Course")
        print("  0. Back to Main Menu")
        print("=" * 60)

        choice = input("  Select option: ").strip()

        if choice == '1':
            view_student_enrollments()
        elif choice == '2':
            enroll_new_student()
        elif choice == '3':
            withdraw_enrolled_student()
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def view_student_enrollments():
    """Displays all enrollments for a specific student."""
    print_header("VIEW STUDENT ENROLLMENTS")

    student_id = get_valid_input("  Enter Student ID: ", input_type=int)
    if student_id is None:
        return

    enrollments = get_enrollments_by_student(student_id)

    if not enrollments:
        print(f"No enrollments found for student {student_id}.")
        press_enter_to_continue()
        return

    widths = [8, 10, 30, 15, 12]
    headers = ['Enroll ID', 'Code', 'Course Name',
               'Date', 'Status']
    print_row(headers, widths)
    print("-" * 60)

    for enrollment in enrollments:
        print_row(enrollment, widths)

    print(f"\nTotal enrollments: {len(enrollments)}")
    press_enter_to_continue()


def enroll_new_student():
    """Enrolls a student in a course."""
    print_header("ENROLL STUDENT IN COURSE")

    student_id = get_valid_input("  Enter Student ID: ", input_type=int)
    if student_id is None:
        return

    course_id = get_valid_input("  Enter Course ID: ", input_type=int)
    if course_id is None:
        return

    enroll_student(student_id, course_id)
    press_enter_to_continue()


def withdraw_enrolled_student():
    """Withdraws a student from an enrollment."""
    print_header("WITHDRAW STUDENT FROM COURSE")

    enrollment_id = get_valid_input(
        "  Enter Enrollment ID: ", input_type=int
    )
    if enrollment_id is None:
        return

    confirm = input(
        f"  Withdraw enrollment {enrollment_id}? (yes/no): "
    ).strip().lower()

    if confirm == 'yes':
        withdraw_student(enrollment_id)
    else:
        print("  Withdrawal cancelled.")

    press_enter_to_continue()


# =============================================================================
# SECTION 4: Grades Management
# =============================================================================

def grades_menu():
    """Grades management sub-menu."""
    while True:
        print_header("GRADES MANAGEMENT")
        print("  1. View Student Grades")
        print("  2. Record Grade")
        print("  3. View Failing Students")
        print("  4. View Top Performing Students")
        print("  0. Back to Main Menu")
        print("=" * 60)

        choice = input("  Select option: ").strip()

        if choice == '1':
            view_student_grades()
        elif choice == '2':
            add_grade_record()
        elif choice == '3':
            view_failing_students()
        elif choice == '4':
            view_top_students()
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def view_student_grades():
    """Displays all grades for a specific student."""
    print_header("VIEW STUDENT GRADES")

    student_id = get_valid_input("  Enter Student ID: ", input_type=int)
    if student_id is None:
        return

    grades = get_grades_by_student(student_id)

    if not grades:
        print(f"No grades found for student {student_id}.")
        press_enter_to_continue()
        return

    widths = [6, 10, 25, 8, 8, 6, 15]
    headers = ['ID', 'Code', 'Course Name',
               'Grade', 'Score', 'GPA', 'Date']
    print_row(headers, widths)
    print("-" * 60)

    for grade in grades:
        print_row(grade, widths)

    press_enter_to_continue()


def add_grade_record():
    """Records a grade for a specific enrollment."""
    print_header("RECORD GRADE")

    try:
        enrollment_id    = get_valid_input(
                             "  Enter Enrollment ID: ",
                             input_type=int
                           )
        if enrollment_id is None:
            return

        letter_grade     = input("  Letter Grade (A/B/C/D/F): ").strip().upper()
        percentage_score = get_valid_input(
                             "  Percentage Score (0-100): ",
                             input_type=float
                           )
        gpa_value        = get_valid_input(
                             "  GPA Value (0.0-4.0): ",
                             input_type=float
                           )

        record_grade(
            enrollment_id, letter_grade,
            percentage_score, gpa_value
        )

    except KeyboardInterrupt:
        print("\nOperation cancelled.")

    press_enter_to_continue()


def view_failing_students():
    """Displays all failing students."""
    print_header("FAILING STUDENTS")
    students = get_failing_students()

    if not students:
        print("No failing students found.")
        press_enter_to_continue()
        return

    widths = [6, 25, 25, 6, 8, 6, 8]
    headers = ['ID', 'Full Name', 'Program',
               'Year', 'Avg Grade', 'GPA', 'Attendance']
    print_row(headers, widths)
    print("-" * 60)

    for student in students:
        print_row(student, widths)

    print(f"\nTotal failing students: {len(students)}")
    press_enter_to_continue()


def view_top_students():
    """Displays all top performing students."""
    print_header("TOP PERFORMING STUDENTS")
    students = get_top_performing_students()

    if not students:
        print("No top performing students found.")
        press_enter_to_continue()
        return

    widths = [6, 25, 25, 6, 8, 6, 8]
    headers = ['ID', 'Full Name', 'Program',
               'Year', 'Avg Grade', 'GPA', 'Attendance']
    print_row(headers, widths)
    print("-" * 60)

    for student in students:
        print_row(student, widths)

    print(f"\nTotal top students: {len(students)}")
    press_enter_to_continue()


# =============================================================================
# SECTION 5: Attendance Management
# =============================================================================

def attendance_menu():
    """Attendance management sub-menu."""
    while True:
        print_header("ATTENDANCE MANAGEMENT")
        print("  1. View Student Attendance")
        print("  2. Record Attendance")
        print("  3. View Attendance Summary")
        print("  0. Back to Main Menu")
        print("=" * 60)

        choice = input("  Select option: ").strip()

        if choice == '1':
            view_student_attendance()
        elif choice == '2':
            add_attendance_record()
        elif choice == '3':
            view_full_attendance_summary()
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


def view_student_attendance():
    """Displays attendance summary for a specific student."""
    print_header("VIEW STUDENT ATTENDANCE")

    student_id = get_valid_input("  Enter Student ID: ", input_type=int)
    if student_id is None:
        return

    attendance = get_attendance_by_student(student_id)

    if not attendance:
        print(f"No attendance records found for student {student_id}.")
        press_enter_to_continue()
        return

    widths = [10, 25, 8, 8, 8, 8, 10]
    headers = ['Code', 'Course Name', 'Total',
               'Present', 'Absent', 'Rate', 'Standing']
    print_row(headers, widths)
    print("-" * 60)

    for record in attendance:
        print_row(record, widths)

    press_enter_to_continue()


def add_attendance_record():
    """Records attendance for a specific enrollment."""
    print_header("RECORD ATTENDANCE")

    try:
        enrollment_id   = get_valid_input(
                            "  Enter Enrollment ID: ",
                            input_type=int
                          )
        if enrollment_id is None:
            return

        attendance_date = input(
            "  Attendance Date (YYYY-MM-DD): "
        ).strip()

        status          = get_valid_input(
                            "  Status (Present/Absent/Late/Excused): ",
                            valid_options=[
                                'Present', 'Absent',
                                'Late', 'Excused'
                            ]
                          )
        if status is None:
            return

        notes = input(
            "  Notes (optional — press Enter to skip): "
        ).strip() or None

        record_attendance(enrollment_id, attendance_date, status, notes)

    except KeyboardInterrupt:
        print("\nOperation cancelled.")

    press_enter_to_continue()


def view_full_attendance_summary():
    """Displays full attendance summary for all students."""
    print_header("FULL ATTENDANCE SUMMARY")
    attendance = get_attendance_summary()

    if not attendance:
        print("No attendance data found.")
        press_enter_to_continue()
        return

    widths = [25, 10, 25, 8, 8, 8, 10]
    headers = ['Full Name', 'Code', 'Course Name',
               'Total', 'Present', 'Rate', 'Standing']
    print_row(headers, widths)
    print("-" * 60)

    for record in attendance:
        print_row(record, widths)

    press_enter_to_continue()


# =============================================================================
# SECTION 6: CSV Export Functions
# =============================================================================

def export_students():
    """Exports all students to CSV."""
    print_header("EXPORT STUDENTS TO CSV")
    from etl.extract import extract_students
    from etl.transform import transform_students
    from etl.load import export_students_csv
    df = transform_students(extract_students())
    export_students_csv(df)
    press_enter_to_continue()


def export_grades():
    """Exports all grades to CSV."""
    print_header("EXPORT GRADES TO CSV")
    from etl.extract import extract_grades
    from etl.transform import transform_grades
    from etl.load import export_grades_csv
    df = transform_grades(extract_grades())
    export_grades_csv(df)
    press_enter_to_continue()


def export_failing():
    """Exports failing students to CSV."""
    print_header("EXPORT FAILING STUDENTS TO CSV")
    from etl.extract import extract_student_summary
    from etl.transform import transform_student_summary
    from etl.load import export_failing_students_csv
    df = transform_student_summary(extract_student_summary())
    failing = df[df['average_grade'] < 50]
    export_failing_students_csv(failing)
    press_enter_to_continue()


def export_top():
    """Exports top performing students to CSV."""
    print_header("EXPORT TOP STUDENTS TO CSV")
    from etl.extract import extract_student_summary
    from etl.transform import transform_student_summary
    from etl.load import export_top_students_csv
    df = transform_student_summary(extract_student_summary())
    top = df[df['average_grade'] >= 75]
    export_top_students_csv(top)
    press_enter_to_continue()


def export_attendance():
    """Exports attendance summary to CSV."""
    print_header("EXPORT ATTENDANCE TO CSV")
    from etl.extract import extract_attendance
    from etl.transform import transform_attendance
    from etl.load import export_attendance_csv
    df = transform_attendance(extract_attendance())
    export_attendance_csv(df)
    press_enter_to_continue()


# =============================================================================
# SECTION 7: Reports Menu
# =============================================================================

def reports_menu():
    """Reports sub-menu."""
    while True:
        print_header("REPORTS")
        print("  1. View Failing Students")
        print("  2. View Top Performing Students")
        print("  3. View Full Attendance Summary")
        print("  4. View Course Enrollment Summary")
        print("  5. Export Students to CSV")
        print("  6. Export Grades to CSV")
        print("  7. Export Failing Students to CSV")
        print("  8. Export Top Students to CSV")
        print("  9. Export Attendance to CSV")
        print("  0. Back to Main Menu")
        print("=" * 60)

        choice = input("  Select option: ").strip()

        if choice == '1':
            view_failing_students()
        elif choice == '2':
            view_top_students()
        elif choice == '3':
            view_full_attendance_summary()
        elif choice == '4':
            view_course_enrollment_summary()
        elif choice == '5':
            export_students()
        elif choice == '6':
            export_grades()
        elif choice == '7':
            export_failing()
        elif choice == '8':
            export_top()
        elif choice == '9':
            export_attendance()
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")


# =============================================================================
# SECTION 8: ETL Pipeline
# =============================================================================

def run_etl_pipeline():
    """Runs the full ETL pipeline from the CLI."""
    print_header("ETL PIPELINE")
    print("  Running full ETL pipeline...")
    print("  This may take a moment.\n")

    try:
        from etl.pipeline import run_pipeline
        run_pipeline()
    except Exception as e:
        print(f"  Pipeline error: {e}")

    press_enter_to_continue()


# =============================================================================
# SECTION 9: Main Menu
# =============================================================================

def main_menu():
    """
    Main menu of the Student Records Management System CLI.
    Entry point for all system operations.
    """
    while True:
        clear_screen()
        print("\n" + "=" * 60)
        print("  STUDENT RECORDS MANAGEMENT SYSTEM")
        print("  Azure PostgreSQL — University Records")
        print("=" * 60)
        print("  1. Student Management")
        print("  2. Course Management")
        print("  3. Enrollment Management")
        print("  4. Grades Management")
        print("  5. Attendance Management")
        print("  6. Reports")
        print("  7. Run ETL Pipeline")
        print("  0. Exit")
        print("=" * 60)

        choice = input("  Select option: ").strip()

        if choice == '1':
            student_menu()
        elif choice == '2':
            course_menu()
        elif choice == '3':
            enrollment_menu()
        elif choice == '4':
            grades_menu()
        elif choice == '5':
            attendance_menu()
        elif choice == '6':
            reports_menu()
        elif choice == '7':
            run_etl_pipeline()
        elif choice == '0':
            print("\n  Exiting system. Goodbye.\n")
            sys.exit(0)
        else:
            print("  Invalid option. Please try again.")


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    """
    Application entry point.
    Tests database connection then launches the main menu.
    """
    clear_screen()
    print("\n" + "=" * 60)
    print("  STUDENT RECORDS MANAGEMENT SYSTEM")
    print("  Initialising...")
    print("=" * 60)

    print("\n  Testing database connection...")
    if not test_connection():
        print("\n  Cannot connect to database.")
        print("  Please check your .env configuration.")
        sys.exit(1)

    print("\n  System ready.")
    press_enter_to_continue()
    main_menu()


if __name__ == '__main__':
    main()