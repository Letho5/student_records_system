# =============================================================================
# STUDENT RECORDS MANAGEMENT SYSTEM
# File: etl/load.py
# Purpose: Loads transformed data into Excel reports.
# =============================================================================

import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# -----------------------------------------------------------------------------
# Output directory configuration
# -----------------------------------------------------------------------------
BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR      = os.path.join(BASE_DIR, 'data', 'processed')


def ensure_output_directory():
    """
    Creates the output directory if it does not already exist.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

# =============================================================================
# SECTION 2: Load Functions
# =============================================================================

def load_to_excel(df, filename, sheet_name='Data'):
    """
    Writes a single DataFrame to an Excel file.
    """
    if df.empty:
        print(f"No data to write for {filename}.")
        return

    ensure_output_directory()
    filepath = os.path.join(OUTPUT_DIR, filename)

    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Auto-adjust column widths for readability
        worksheet = writer.sheets[sheet_name]
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 4, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

    print(f"Saved: {filepath}")


def load_students(df):
    """
    Loads transformed student data to Excel.
    """
    load_to_excel(df, 'students.xlsx', sheet_name='Students')


def load_courses(df):
    """
    Loads transformed course data to Excel.
    """
    load_to_excel(df, 'courses.xlsx', sheet_name='Courses')


def load_enrollments(df):
    """
    Loads transformed enrollment data to Excel.
    """
    load_to_excel(df, 'enrollments.xlsx', sheet_name='Enrollments')


def load_grades(df):
    """
    Loads transformed grade data to Excel.
    """
    load_to_excel(df, 'grades.xlsx', sheet_name='Grades')


def load_attendance(df):
    """
    Loads transformed attendance data to Excel.
    """
    load_to_excel(df, 'attendance.xlsx', sheet_name='Attendance')


def load_student_summary(df):
    """
    Loads transformed student summary data to Excel.
    """
    load_to_excel(df, 'student_summary.xlsx', sheet_name='Student Summary')


def load_full_report(students_df, courses_df, enrollments_df,
                     grades_df, attendance_df, summary_df):
    """
    Writes all DataFrames into a single comprehensive Excel workbook
    with one sheet per dataset.
    """
    if all(df.empty for df in [students_df, courses_df, enrollments_df,
                                grades_df, attendance_df, summary_df]):
        print("No data available to generate full report.")
        return

    ensure_output_directory()
    filepath = os.path.join(OUTPUT_DIR, 'full_report.xlsx')

    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        datasets = [
            (students_df,     'Students'),
            (courses_df,      'Courses'),
            (enrollments_df,  'Enrollments'),
            (grades_df,       'Grades'),
            (attendance_df,   'Attendance'),
            (summary_df,      'Student Summary'),
        ]

        for df, sheet_name in datasets:
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

                # Auto-adjust column widths
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 4, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width

                print(f"  Sheet written: {sheet_name} ({len(df)} records)")

    print(f"\nFull report saved: {filepath}")

# =============================================================================
# CSV EXPORT FUNCTIONS
# =============================================================================

def export_to_csv(df, filename):
    """
    Writes a single DataFrame to a CSV file in the processed folder.
    """
    if df.empty:
        print(f"No data to export for {filename}.")
        return False

    ensure_output_directory()
    filepath = os.path.join(OUTPUT_DIR, filename)

    df.to_csv(filepath, index=False)
    print(f"CSV exported: {filepath}")
    return True


def export_students_csv(df):
    """Exports student data to CSV."""
    export_to_csv(df, 'students_export.csv')


def export_grades_csv(df):
    """Exports grades data to CSV."""
    export_to_csv(df, 'grades_export.csv')


def export_failing_students_csv(df):
    """Exports failing students data to CSV."""
    export_to_csv(df, 'failing_students_export.csv')


def export_top_students_csv(df):
    """Exports top performing students data to CSV."""
    export_to_csv(df, 'top_students_export.csv')


def export_attendance_csv(df):
    """Exports attendance summary data to CSV."""
    export_to_csv(df, 'attendance_summary_export.csv')