# database.py
import sqlite3

def create_connection():
    conn = sqlite3.connect('sekolah.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    
    # Tabel Siswa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            class_id INTEGER,
            FOREIGN KEY (class_id) REFERENCES classes (id)
        )
    ''')
    
    # Tabel Nilai
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            score INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    # Tabel Kehadiran
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    # Tabel Peminjaman Buku
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS library_loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            book_title TEXT NOT NULL,
            loan_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_student(name, age, class_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, class_id) VALUES (?, ?, ?)", (name, age, class_id))
    conn.commit()
    conn.close()

def get_students():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return students

def delete_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()

def add_grade(student_id, subject, score):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO grades (student_id, subject, score) VALUES (?, ?, ?)', (student_id, subject, score))
    conn.commit()
    conn.close()

def get_grades():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT grades.id, students.name, grades.subject, grades.score FROM grades JOIN students ON grades.student_id = students.id')
    grades = cursor.fetchall()
    conn.close()
    return grades

def add_attendance(student_id, date, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)', (student_id, date, status))
    conn.commit()
    conn.close()

def get_attendance():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT attendance.id, students.name, attendance.date, attendance.status FROM attendance JOIN students ON attendance.student_id = students.id')
    attendance = cursor.fetchall()
    conn.close()
    return attendance

def add_library_loan(student_id, book_title, loan_date):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO library_loans (student_id, book_title, loan_date) VALUES (?, ?, ?)', (student_id, book_title, loan_date))
    conn.commit()
    conn.close()

def get_library_loans():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT library_loans.id, students.name, library_loans.book_title, library_loans.loan_date, library_loans.return_date FROM library_loans JOIN students ON library_loans.student_id = students.id')
    loans = cursor.fetchall()
    conn.close()
    return loans

def add_class(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO classes (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def get_classes():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM classes')
    classes = cursor.fetchall()
    conn.close()
    return classes