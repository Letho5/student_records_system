# =============================================================================
# STUDENT RECORDS MANAGEMENT SYSTEM
# File: etl/transform.py
# Purpose: Transforms raw extracted data into clean, structured DataFrames.
# =============================================================================

import pandas as pd
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# -----------------------------------------------------------------------------
# Grade boundary reference — used for classification
# -----------------------------------------------------------------------------
GRADE_BOUNDARIES = {
    'A':  (90, 100),
    'B':  (80, 89),
    'C':  (70, 79),
    'D':  (60, 69),
    'F':  (0,  59)
}

# =============================================================================
# SECTION 2: Transform Functions
# =============================================================================

def transform_students(df):
    """
    Cleans and enriches the raw students DataFrame.
    Returns a transformed pandas DataFrame.
    """
    if df.empty:
        print("No student data to transform.")
        return df

    # Remove duplicates
    df = df.drop_duplicates(subset=['student_id'])

    # Create full name column
    df['full_name'] = df['first_name'] + ' ' + df['last_name']

    # Ensure correct data types
    df['date_of_birth']   = pd.to_datetime(df['date_of_birth'])
    df['enrollment_date'] = pd.to_datetime(df['enrollment_date'])

    # Calculate student age
    today = pd.Timestamp.today()
    df['age'] = ((today - df['date_of_birth']).dt.days / 365.25).astype(int)

    # Reorder columns cleanly
    df = df[[
        'student_id', 'full_name', 'first_name', 'last_name',
        'date_of_birth', 'age', 'gender', 'email', 'phone_number',
        'program', 'year_of_study', 'status', 'enrollment_date'
    ]]

    print(f"Transformed {len(df)} student records.")
    return df


def transform_courses(df):
    """
    Cleans and enriches the raw courses DataFrame.
    Returns a transformed pandas DataFrame.
    """
    if df.empty:
        print("No course data to transform.")
        return df

    # Remove duplicates
    df = df.drop_duplicates(subset=['course_id'])

    # Ensure correct data types
    df['credits']      = df['credits'].astype(int)
    df['max_students'] = df['max_students'].astype(int)

    # Add credit classification
    df['credit_level'] = df['credits'].apply(
        lambda x: 'Light' if x <= 2 else ('Standard' if x <= 4 else 'Heavy')
    )

    # Reorder columns cleanly
    df = df[[
        'course_id', 'course_code', 'course_name',
        'department', 'credits', 'credit_level',
        'semester', 'max_students'
    ]]

    print(f"Transformed {len(df)} course records.")
    return df


def transform_enrollments(df):
    """
    Cleans and enriches the raw enrollments DataFrame.
    Returns a transformed pandas DataFrame.
    """
    if df.empty:
        print("No enrollment data to transform.")
        return df

    # Remove duplicates
    df = df.drop_duplicates(subset=['enrollment_id'])

    # Ensure correct data types
    df['enrollment_date'] = pd.to_datetime(df['enrollment_date'])

    # Add full name column
    df['full_name'] = df['first_name'] + ' ' + df['last_name']

    # Reorder columns cleanly
    df = df[[
        'enrollment_id', 'student_id', 'full_name',
        'course_id', 'course_code', 'course_name',
        'enrollment_date', 'status'
    ]]

    print(f"Transformed {len(df)} enrollment records.")
    return df


def transform_grades(df):
    """
    Cleans and enriches the raw grades DataFrame.
    Returns a transformed pandas DataFrame.
    """
    if df.empty:
        print("No grade data to transform.")
        return df

    # Remove duplicates
    df = df.drop_duplicates(subset=['grade_id'])

    # Ensure correct data types
    df['percentage_score'] = pd.to_numeric(df['percentage_score'], errors='coerce')
    df['gpa_value']        = pd.to_numeric(df['gpa_value'], errors='coerce')
    df['date_recorded']    = pd.to_datetime(df['date_recorded'])

    # Add full name column
    df['full_name'] = df['first_name'] + ' ' + df['last_name']

    # Add performance classification
    df['performance'] = df['percentage_score'].apply(classify_performance)

    # Reorder columns cleanly
    df = df[[
        'grade_id', 'enrollment_id', 'full_name',
        'course_code', 'course_name', 'letter_grade',
        'percentage_score', 'gpa_value', 'performance',
        'date_recorded'
    ]]

    print(f"Transformed {len(df)} grade records.")
    return df


def transform_attendance(df):
    """
    Cleans and enriches the raw attendance DataFrame.
    Returns a transformed pandas DataFrame.
    """
    if df.empty:
        print("No attendance data to transform.")
        return df

    # Remove duplicates
    df = df.drop_duplicates(subset=['attendance_id'])

    # Ensure correct data types
    df['attendance_date'] = pd.to_datetime(df['attendance_date'])

    # Add full name column
    df['full_name'] = df['first_name'] + ' ' + df['last_name']

    # Add present flag for easy calculation
    df['is_present'] = df['status'].apply(
        lambda x: 1 if x == 'Present' else 0
    )

    # Reorder columns cleanly
    df = df[[
        'attendance_id', 'enrollment_id', 'full_name',
        'course_code', 'course_name', 'attendance_date',
        'status', 'is_present', 'notes'
    ]]

    print(f"Transformed {len(df)} attendance records.")
    return df


def transform_student_summary(df):
    """
    Cleans and enriches the student summary DataFrame.
    Returns a transformed pandas DataFrame.
    """
    if df.empty:
        print("No summary data to transform.")
        return df

    # Remove duplicates
    df = df.drop_duplicates(subset=['student_id'])

    # Fill missing values for students with no grades or attendance
    df['average_grade']    = df['average_grade'].fillna(0)
    df['average_gpa']      = df['average_gpa'].fillna(0)
    df['attendance_rate']  = df['attendance_rate'].fillna(0)
    df['total_sessions']   = df['total_sessions'].fillna(0)
    df['sessions_present'] = df['sessions_present'].fillna(0)

    # Ensure correct data types
    df['average_grade']    = df['average_grade'].astype(float)
    df['average_gpa']      = df['average_gpa'].astype(float)
    df['attendance_rate']  = df['attendance_rate'].astype(float)

    # Add full name
    df['full_name'] = df['first_name'] + ' ' + df['last_name']

    # Add performance classification
    df['performance'] = df['average_grade'].apply(classify_performance)

    # Add attendance classification
    df['attendance_standing'] = df['attendance_rate'].apply(
        lambda x: 'Excellent' if x >= 90 else (
                  'Good'      if x >= 75 else (
                  'At Risk'   if x >= 60 else 'Critical'))
    )

    # Reorder columns cleanly
    df = df[[
        'student_id', 'full_name', 'program', 'year_of_study',
        'status', 'total_enrollments', 'average_grade',
        'average_gpa', 'performance', 'attendance_rate',
        'attendance_standing'
    ]]

    print(f"Transformed {len(df)} student summary records.")
    return df


# -----------------------------------------------------------------------------
# Helper Function
# -----------------------------------------------------------------------------
def classify_performance(score):
    """
    Classifies a percentage score into a performance category.
    """
    if score >= 90:   return 'Distinction'
    elif score >= 80: return 'Merit'
    elif score >= 70: return 'Pass'
    elif score >= 60: return 'Below Average'
    else:             return 'Fail'