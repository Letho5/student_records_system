# =============================================================================
# STUDENT RECORDS MANAGEMENT SYSTEM
# File: etl/pipeline.py
# Purpose: Orchestrates the complete ETL pipeline.
#          Runs Extract, Transform and Load in sequence.
# =============================================================================

import warnings
warnings.filterwarnings('ignore', category=UserWarning)

from etl.extract import (
    extract_students,
    extract_courses,
    extract_enrollments,
    extract_grades,
    extract_attendance,
    extract_student_summary
)

from etl.transform import (
    transform_students,
    transform_courses,
    transform_enrollments,
    transform_grades,
    transform_attendance,
    transform_student_summary
)

from etl.load import (
    load_students,
    load_courses,
    load_enrollments,
    load_grades,
    load_attendance,
    load_student_summary,
    load_full_report
)


# =============================================================================
# Pipeline Execution Function
# =============================================================================

def run_pipeline():
    """
    Executes the complete ETL pipeline in sequence.
    Extracts all data from Azure PostgreSQL, transforms it
    and loads it into Excel reports.
    """

    print("=" * 60)
    print("STUDENT RECORDS SYSTEM — ETL Pipeline")
    print("=" * 60)

    # -------------------------------------------------------------------------
    # EXTRACT
    # -------------------------------------------------------------------------
    print("\n[ EXTRACT ]")
    raw_students    = extract_students()
    raw_courses     = extract_courses()
    raw_enrollments = extract_enrollments()
    raw_grades      = extract_grades()
    raw_attendance  = extract_attendance()
    raw_summary     = extract_student_summary()

    # -------------------------------------------------------------------------
    # TRANSFORM
    # -------------------------------------------------------------------------
    print("\n[ TRANSFORM ]")
    students    = transform_students(raw_students)
    courses     = transform_courses(raw_courses)
    enrollments = transform_enrollments(raw_enrollments)
    grades      = transform_grades(raw_grades)
    attendance  = transform_attendance(raw_attendance)
    summary     = transform_student_summary(raw_summary)

    # -------------------------------------------------------------------------
    # LOAD
    # -------------------------------------------------------------------------
    print("\n[ LOAD ]")
    load_students(students)
    load_courses(courses)
    load_enrollments(enrollments)
    load_grades(grades)
    load_attendance(attendance)
    load_student_summary(summary)

    # -------------------------------------------------------------------------
    # Full Report
    # -------------------------------------------------------------------------
    print("\n[ FULL REPORT ]")
    load_full_report(
        students,
        courses,
        enrollments,
        grades,
        attendance,
        summary
    )

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("ETL PIPELINE COMPLETE")
    print("=" * 60)
    print(f"  Students:    {len(students)} records")
    print(f"  Courses:     {len(courses)} records")
    print(f"  Enrollments: {len(enrollments)} records")
    print(f"  Grades:      {len(grades)} records")
    print(f"  Attendance:  {len(attendance)} records")
    print(f"  Summary:     {len(summary)} records")
    print("=" * 60)
    print("\nAll reports saved to: data/processed/")


# =============================================================================
# Entry Point
# =============================================================================
if __name__ == '__main__':
    run_pipeline()