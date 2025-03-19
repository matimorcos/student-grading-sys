# Student Grading System
This application has been developed to optimize the flipped classroom model in virtual learning environments. It features a comprehensive CRUD system for students, subjects, practical assignments, and grades based on various evaluation criteria that make up each assignment. This allows teachers to enter student, subject, and assignment data only once per academic period and grade their students as they review their submissions.

# CRM feature
Additionally, the system enables automated feedback by sending an email with comments based on the assigned grade. This tool has been implemented at Universidad Empresarial Siglo 21 and has been highly recognized as an innovative solution for automating preliminary feedback to students upon submission of their assignments. By providing immediate feedback, it offers students a valuable opportunity to correct mistakes and deepen their understanding, not only optimizing response times but also enriching their learning experience.

# Flexibility
Moreover, this system reduces administrative workload, allowing educators to focus on qualitative aspects of teaching, improving classroom dynamics, and enhancing education. As a result, it contributes to a more efficient and effective learning process.

While it was specifically designed for Universidad Empresarial Siglo 21, the database models can be redesigned using SQLAlchemy and Alembic for migrations. The system is intended for practical use by teachers without the need to expose student data through a web frontend. Instead, feedback is maintained via a microservice, allowing modifications directly from the backend based on the needs of the institution, the teacher, or the subject, like data analytics asynchronus tasks by Python integrated libraries.
