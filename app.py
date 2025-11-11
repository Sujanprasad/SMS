from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('school.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# --- Students ---
@app.route('/students')
def students():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('students.html', students=data)

@app.route('/students/add', methods=('GET', 'POST'))
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        dept = request.form['department']
        conn = get_db_connection()
        conn.execute('INSERT INTO students (name, age, department) VALUES (?, ?, ?)',
                     (name, age, dept))
        conn.commit()
        conn.close()
        return redirect(url_for('students'))
    return render_template('add_student.html')

# --- Courses ---
@app.route('/courses')
def courses():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()
    return render_template('courses.html', courses=data)

@app.route('/courses/add', methods=('GET', 'POST'))
def add_course():
    if request.method == 'POST':
        cname = request.form['course_name']
        credits = request.form['credits']
        conn = get_db_connection()
        conn.execute('INSERT INTO courses (course_name, credits) VALUES (?, ?)',
                     (cname, credits))
        conn.commit()
        conn.close()
        return redirect(url_for('courses'))
    return render_template('add_course.html')

# --- Enrollments ---
@app.route('/enrollments')
def enrollments():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    courses = conn.execute('SELECT * FROM courses').fetchall()
    enrollments = conn.execute('''
        SELECT e.id, s.name AS student_name, c.course_name 
        FROM enrollments e
        JOIN students s ON e.student_id = s.id
        JOIN courses c ON e.course_id = c.id
    ''').fetchall()
    conn.close()
    return render_template('enrollments.html',
                           students=students,
                           courses=courses,
                           enrollments=enrollments)

@app.route('/enroll', methods=('POST',))
def enroll():
    student_id = request.form['student_id']
    course_id = request.form['course_id']
    conn = get_db_connection()
    conn.execute('INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)',
                 (student_id, course_id))
    conn.commit()
    conn.close()
    return redirect(url_for('enrollments'))

if __name__ == '__main__':
    app.run(debug=True)
