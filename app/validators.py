# =============================================================================
# STUDENT RECORDS MANAGEMENT SYSTEM
# File: app/validators.py
# Purpose: Input validation functions for all user-facing data entry.
# =============================================================================

import re
from datetime import datetime


# =============================================================================
# SECTION 1: Name Validation
# =============================================================================

def validate_name(name, field_name='Name'):
    """
    Validates that a name field is not empty and contains
    only letters, spaces and hyphens.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    if not name or not name.strip():
        return False, f"{field_name} cannot be empty."

    if len(name.strip()) < 2:
        return False, f"{field_name} must be at least 2 characters."

    if len(name.strip()) > 50:
        return False, f"{field_name} cannot exceed 50 characters."

    if not re.match(r"^[A-Za-z\s\-']+$", name.strip()):
        return False, f"{field_name} can only contain letters, spaces and hyphens."

    return True, None


# =============================================================================
# SECTION 2: Email Validation
# =============================================================================

def validate_email(email):
    """
    Validates that an email address is correctly formatted.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    if not email or not email.strip():
        return False, "Email address cannot be empty."

    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, email.strip()):
        return False, "Invalid email format. Example: john.doe@university.ac.za"

    if len(email.strip()) > 100:
        return False, "Email address cannot exceed 100 characters."

    return True, None


# =============================================================================
# SECTION 3: Date Validation
# =============================================================================

def validate_date(date_string, field_name='Date'):
    """
    Validates that a date string is in YYYY-MM-DD format
    and represents a real calendar date.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    if not date_string or not date_string.strip():
        return False, f"{field_name} cannot be empty."

    try:
        parsed_date = datetime.strptime(date_string.strip(), '%Y-%m-%d')
        return True, None
    except ValueError:
        return False, f"{field_name} must be in YYYY-MM-DD format. Example: 2024-01-15"


def validate_date_of_birth(date_string):
    """
    Validates date of birth.
    Student must be between 15 and 60 years old.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    valid, error = validate_date(date_string, 'Date of birth')
    if not valid:
        return False, error

    dob = datetime.strptime(date_string.strip(), '%Y-%m-%d')
    today = datetime.today()
    age = (today - dob).days / 365.25

    if age < 15:
        return False, "Student must be at least 15 years old."

    if age > 60:
        return False, "Date of birth appears incorrect. Age exceeds 60 years."

    return True, None


def validate_attendance_date(date_string):
    """
    Validates an attendance date.
    Cannot be a future date.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    valid, error = validate_date(date_string, 'Attendance date')
    if not valid:
        return False, error

    attendance_date = datetime.strptime(date_string.strip(), '%Y-%m-%d')
    today = datetime.today()

    if attendance_date > today:
        return False, "Attendance date cannot be in the future."

    return True, None


# =============================================================================
# SECTION 4: Grade Validation
# =============================================================================

def validate_grade_score(score):
    """
    Validates that a percentage score is between 0 and 100.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    try:
        score_float = float(score)
    except (ValueError, TypeError):
        return False, "Grade score must be a number."

    if score_float < 0 or score_float > 100:
        return False, "Grade score must be between 0 and 100."

    return True, None


def validate_gpa(gpa):
    """
    Validates that a GPA value is between 0.0 and 4.0.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    try:
        gpa_float = float(gpa)
    except (ValueError, TypeError):
        return False, "GPA value must be a number."

    if gpa_float < 0 or gpa_float > 4:
        return False, "GPA value must be between 0.0 and 4.0."

    return True, None


def validate_letter_grade(grade):
    """
    Validates that a letter grade is one of the accepted values.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    valid_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']

    if not grade or not grade.strip():
        return False, "Letter grade cannot be empty."

    if grade.strip().upper() not in valid_grades:
        return False, f"Invalid letter grade. Must be one of: {', '.join(valid_grades)}"

    return True, None


# =============================================================================
# SECTION 5: Student Field Validation
# =============================================================================

def validate_year_of_study(year):
    """
    Validates that year of study is between 1 and 6.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    try:
        year_int = int(year)
    except (ValueError, TypeError):
        return False, "Year of study must be a whole number."

    if year_int < 1 or year_int > 6:
        return False, "Year of study must be between 1 and 6."

    return True, None


def validate_student_status(status):
    """
    Validates that a student status is one of the accepted values.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    valid_statuses = ['Active', 'Inactive', 'Graduated', 'Suspended']

    if not status or not status.strip():
        return False, "Status cannot be empty."

    if status.strip() not in valid_statuses:
        return False, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"

    return True, None


def validate_gender(gender):
    """
    Validates that gender is one of the accepted values.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    valid_genders = ['Male', 'Female', 'Other']

    if not gender or not gender.strip():
        return False, "Gender cannot be empty."

    if gender.strip() not in valid_genders:
        return False, f"Invalid gender. Must be one of: {', '.join(valid_genders)}"

    return True, None


def validate_phone(phone):
    """
    Validates that a phone number is reasonable.
    Phone number is optional so empty is allowed.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    if not phone or not phone.strip():
        return True, None

    if len(phone.strip()) > 20:
        return False, "Phone number cannot exceed 20 characters."

    return True, None


# =============================================================================
# SECTION 6: Course Field Validation
# =============================================================================

def validate_credits(credits):
    """
    Validates that credits are between 1 and 8.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    try:
        credits_int = int(credits)
    except (ValueError, TypeError):
        return False, "Credits must be a whole number."

    if credits_int < 1 or credits_int > 8:
        return False, "Credits must be between 1 and 8."

    return True, None


def validate_semester(semester):
    """
    Validates that semester is one of the accepted values.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    valid_semesters = ['Semester 1', 'Semester 2', 'Full Year']

    if not semester or not semester.strip():
        return False, "Semester cannot be empty."

    if semester.strip() not in valid_semesters:
        return False, f"Invalid semester. Must be one of: {', '.join(valid_semesters)}"

    return True, None


def validate_max_students(max_students):
    """
    Validates that max students is a positive number.
    Returns (True, None) if valid.
    Returns (False, error_message) if invalid.
    """
    try:
        max_int = int(max_students)
    except (ValueError, TypeError):
        return False, "Max students must be a whole number."

    if max_int < 1:
        return False, "Max students must be at least 1."

    if max_int > 1000:
        return False, "Max students cannot exceed 1000."

    return True, None


# =============================================================================
# SECTION 7: Composite Validation
# =============================================================================

def validate_new_student(first_name, last_name, date_of_birth,
                          gender, email, phone, program,
                          year_of_study, status, enrollment_date):
    """
    Runs all validations for a new student record.
    Returns (True, None) if all fields are valid.
    Returns (False, error_message) on first validation failure.
    """
    validations = [
        validate_name(first_name, 'First name'),
        validate_name(last_name, 'Last name'),
        validate_date_of_birth(date_of_birth),
        validate_gender(gender),
        validate_email(email),
        validate_phone(phone),
        validate_name(program, 'Program'),
        validate_year_of_study(year_of_study),
        validate_student_status(status),
        validate_date(enrollment_date, 'Enrollment date'),
    ]

    for valid, error in validations:
        if not valid:
            return False, error

    return True, None


def validate_new_course(course_code, course_name, department,
                         credits, semester, max_students):
    """
    Runs all validations for a new course record.
    Returns (True, None) if all fields are valid.
    Returns (False, error_message) on first validation failure.
    """
    validations = [
        validate_name(course_code, 'Course code'),
        validate_name(course_name, 'Course name'),
        validate_name(department, 'Department'),
        validate_credits(credits),
        validate_semester(semester),
        validate_max_students(max_students),
    ]

    for valid, error in validations:
        if not valid:
            return False, error

    return True, None