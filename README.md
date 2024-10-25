# Student Tracking Information System for Vocational Schools

## Abstract

Vocational and technical high schools in Kenya provide training in over 130 occupations. The process of tracking students during their practical training periods involves manual paperwork, which can be cumbersome and inefficient. This project aims to digitalize the current processes by proposing a web-based solution for tracking practical training in vocational and technical high schools in Kenya. This Python project is a Teacher-Student Feedback Management System built with Tkinter.

## Technologies To Be Used
- **Front-End(User Interface)**: Tkinter, PyQt/PySide, Kivy.
- **Back-End(Application Logic)**: Flask/Django, FastAPI.
- **Database(Persistent Storage)**: SQLite, MySQL/PostgreSQL, MongoDB.
- **Authentication & User Management**: Flask-Login or Django's built-in auth system, OAuth2.0 or OpenID Connect.
- **Packaging for Distribution**: PyInstaller, cx_Freeze, Electron with Python Back-End.
- **API Integration**: RESTful APIs, GraphQL.
- **Deployment(if web-based)**: Heroku/PythonAnywhere, Amazon Web Services(AWS)/Google Cloud Platform(GCP)/Microsoft Azure, Docker
- **Version Control & CI/CD**: Github/GitLab, Continous Integration/Continous Deployment(CI/CD).
- **Data Validation and Security**: Encrypting sensitive information using libraries like cryptography, Setting up role-based access control to ensure only authorized users can perform 
  specific actions, and Validating input like phone numbers and emails.

## Functionalities

The Student Tracking Information System offers the following functionalities:

- Manager:
  - Add, delete, and modify teachers, students, and companies.
  - Define username and password for teachers.
  - View all feedback and mark them as controlled or not controlled.

- Teachers:
  - View assigned students with their detailed information.
  - View feedback related to their assigned students.
  - Add, delete, and modify feedback (if not checked by the manager).

## Motivation

The motivation behind this project is to simplify the student tracking process, eliminate paperwork, and provide a paper-free solution. By digitalizing the processes, the system aims to improve communication between teachers, students, and companies, facilitate better supervision, and provide opportunities for students' career development.

## Goal

The goal of this project is to develop the first web-based student tracking system for vocational high schools in Kenya. The system aims to overcome the limitations of existing systems by offering detailed feedback features tailored to the vocational education system in Kenya, providing essential information about students and companies, and utilizing modern technologies for improved performance, security, and visual quality.

## System Functional Requirements

The system caters to two main types of users:

1. **Technical Manager**: Responsible for managing the student tracking process.
2. **Teachers**: Responsible for closely following students during practical training.

The system allows managers to add, delete, and modify teachers, students, and companies. It also enables teachers to view assigned students, view and add feedback, and perform other related actions.

## How to Use

To use the Student Tracking Information System:

1. Clone the repository to your local machine.
2. Set up the required environment for Laravel development (PHP, Composer, MySQL).
3. Configure the database connection in the `.env` file.
4. Run database migrations to create necessary tables.
5. Start the Laravel development server.
6. Access the system via a web browser.

## Contributors

- [James Otipa](https://github.com/Liwei254)

## Clone the repository:
   ```bash
https://github.com/Liwei254/StudentTrackingSystemPython.git
