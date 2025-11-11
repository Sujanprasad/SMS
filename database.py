import sqlite3

connection = sqlite3.connect('school.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# --- Students Data ---
students = [
    ('John Doe', 20, 'Computer Science'),
    ('Emma Watson', 21, 'Electronics'),
    ('Rahul Sharma', 22, 'Mechanical'),
    ('Sophia Davis', 19, 'Civil'),
    ('Arjun Patel', 20, 'Information Tech')
]
cur.executemany("INSERT INTO students (name, age, department) VALUES (?, ?, ?)", students)

# --- Courses Data ---
courses = [
    ('Database Systems', 4),
    ('Operating Systems', 3),
    ('Computer Networks', 3),
    ('Data Structures', 4),
    ('Software Engineering', 3)
]
cur.executemany("INSERT INTO courses (course_name, credits) VALUES (?, ?)", courses)

# --- Enrollments (link student_id and course_id) ---
enrollments = [
    (1, 1),  # John Doe → Database Systems
    (1, 2),  # John Doe → Operating Systems
    (2, 3),  # Emma → Computer Networks
    (3, 1),  # Rahul → Database Systems
    (4, 4),  # Sophia → Data Structures
    (5, 2),  # Arjun → Operating Systems
    (5, 5)   # Arjun → Software Engineering
]
cur.executemany("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", enrollments)

connection.commit()
connection.close()

print("✅ Database setup complete with sample records.")
