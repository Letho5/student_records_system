
# Student Records Management System

A relational database system designed to manage student academic
records across enrollments, grades, and attendance. This project
demonstrates the full data engineering lifecycle — from schema
design and ETL development to a live cloud-hosted database and
an interactive business intelligence dashboard.


## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Database Design](#database-design)
- [Getting Started](#getting-started)
- [ETL Pipeline](#etl-pipeline)
- [Command Line Interface](#command-line-interface)
- [Data Quality and Testing](#data-quality-and-testing)
- [Power BI Dashboard](#power-bi-dashboard)
- [Team](#team)


## Overview

This system was built to simulate how a real university manages
its student data — not as a theoretical exercise, but as something
that could genuinely be deployed and used.

Every decision made in this project, from how the schema is
structured to how data flows through the pipeline, was guided by
the same question: would this hold up in a real environment? We
believe it would.

The database is live on Microsoft Azure and holds 33,617 records
across five tables. The data is accessible through a Python CLI,
queryable through six database views, and visualised through a
connected Power BI dashboard.


## Project Structure

student_records_system/
│
├── app/
│   ├── cli.py
│   ├── crud.py
│   ├── db_connection.py
│   └── validators.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│       └── generate_sample_data.py
│
├── database/
│   ├── schema.sql
│   ├── views.sql
│   ├── procedures.sql
│   ├── indexes.sql
│   └── setup_database.py
│
├── docs/
│   └── StudentRecordsDashboard.pbix
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
│
├── tests/
│   └── test_etl.py
│
├── .env
├── .gitignore
└── requirements.txt



## Technology Stack

The project runs entirely on freely available and industry-standard
tools. No paid libraries, no unnecessary dependencies.

- **Database** — Azure PostgreSQL (cloud-hosted, live)
- **Language** — Python 3.11.9
- **Database Connector** — psycopg2-binary
- **Data Processing** — pandas
- **Sample Data Generation** — Faker
- **Environment Management** — python-dotenv
- **Excel Export** — openpyxl
- **Dashboard** — Power BI Desktop
- **Version Control** — Git and GitHub


## Database Design

The schema is normalised to Third Normal Form. Every table serves
a single, well-defined purpose and every relationship between
tables is enforced through foreign keys.

**The five core tables and their record counts:**

- students — 500 records
- courses — 25 records
- enrollments — 1,250 records
- grades — 1,250 records
- attendance — 31,092 records

Total records in the database: 33,617

**Database Views**

Six views were written to expose pre-joined, query-ready data
to the application and dashboard layers, removing the need for
complex joins at runtime.

- vw_student_overview
- vw_course_enrollment_summary
- vw_student_grades
- vw_attendance_summary
- vw_failing_students
- vw_top_performing_students

**Stored Procedures**

Four stored procedures handle the core write operations in the
system, keeping business logic inside the database where it belongs.

- enroll_student — enrols a student into a course
- record_grade — records a grade against an enrollment
- record_attendance — logs a daily attendance record
- update_student_status — updates a student's current status

**Indexes**

19 indexes were created across all five tables. They target the
columns most frequently used in filtering and joining operations,
including student_id, course_id, enrollment_id, and date fields.


## Getting Started

**Prerequisites**

Before running anything, make sure you have the following in place:

- Python 3.11.9 installed on your machine
- A virtual environment created and activated
- Valid credentials for the Azure PostgreSQL database

**Cloning the Repository**


git clone https://github.com/Letho5/student_records_system.git
cd student_records_system

**Setting Up the Environment**


python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

**Configuring the Database Connection**

Create a file named `.env` in the root of the project and add
the following:


DB_HOST=studentrecordsdb.postgres.database.azure.com
DB_NAME=postgres
DB_USER=exceladmin
DB_PASSWORD=your_password
DB_SSLMODE=require


The `.env` file is listed in `.gitignore` and will never be
committed to the repository.


## ETL Pipeline

The pipeline is split into three stages, each handled by its own
script. This separation makes the code easy to read, test, and
maintain independently.

- **extract.py** reads data from the source files
- **transform.py** cleans, validates and shapes the data
- **load.py** inserts the processed records into Azure PostgreSQL
- **pipeline.py** ties all three stages together and runs them
  in sequence

To run the full pipeline:


python -m etl.pipeline


To regenerate the sample data from scratch:


python data/sample/generate_sample_data.py



## Command Line Interface

A terminal-based CLI was built to allow direct interaction with
the live database. It supports full CRUD operations across all
tables and was designed to be simple enough for non-technical
users to navigate.

To launch the CLI:


python -m app.cli


Through the CLI you can add, view, update and delete student
records, enroll students into courses, record grades and
attendance, and view summaries directly in the terminal.


## Data Quality and Testing

Validation is handled by `validators.py` and covers data types,
required fields, format rules, and referential integrity checks
across all tables before any record touches the database.

The test suite in `tests/test_etl.py` covers the ETL pipeline
end-to-end, including database connectivity, data transformation
logic, and all validation rules.

To run the tests:


python -m tests.test_etl


All 32 tests pass with 0 failures.


## Power BI Dashboard

The dashboard connects directly to the live Azure PostgreSQL
database and refreshes against real data. It is split across
two pages.

**Page 1 — Overview**

An executive-level summary of the student population, built
from five visuals covering total student count, program
distribution, course enrollment, grade distribution, and
attendance standing.

**Page 2 — Student Detail**

Two detailed tables showing the students who are currently
failing and the students who are top performers, pulled
directly from the corresponding database views.

The dashboard file is located at:


docs/StudentRecordsDashboard.pbix



## Team

This system was built by a group of students as part of a
university data engineering course.

We treated this the way we would want to treat real work —
with consistency, attention to detail, and a genuine interest
in building something that actually works. Every phase was
planned and executed with care, from the first line of SQL
to the final Power BI visual.

GitHub Repository: https://github.com/Letho5/student_records_system

