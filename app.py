# app.py
import csv
import io  # Tambahkan ini
from flask import Flask, render_template, request, redirect, make_response
from database import create_tables, add_student, get_students, delete_student, add_grade, get_grades, add_attendance, get_attendance, add_library_loan, get_library_loans, add_class, get_classes
app = Flask(__name__)

create_tables()

# Halaman Siswa
@app.route('/', methods=['GET', 'POST'])
def index():
    classes = get_classes()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        class_id = request.form['class_id']  # Ambil ID kelas dari dropdown
        add_student(name, age, class_id)  # Pastikan fungsi ini menerima class_id
        return redirect('/')
    students = get_students()
    return render_template('index.html', students=students, classes=classes)

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete(student_id):
    delete_student(student_id)
    return redirect('/')

@app.route('/download_students')
def download_students():
    students = get_students()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Nama', 'Usia', 'Kelas'])
    for student in students:
        writer.writerow(student)
    output.seek(0)  # Kembali ke awal objek StringIO
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=students.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

# Halaman Nilai
@app.route('/grades', methods=['GET', 'POST'])
def grades():
    if request.method == 'POST':
        student_id = request.form['student_id']
        subject = request.form['subject']
        score = request.form['score']
        add_grade(student_id, subject, score)
        return redirect('/grades')
    grades = get_grades()
    students = get_students()
    return render_template('grades.html', grades=grades, students=students)

@app.route('/download_grades')
def download_grades():
    grades = get_grades()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Nama Siswa', 'Mata Pelajaran', 'Nilai'])
    for grade in grades:
        writer.writerow(grade)
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=grades.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

# Halaman Kehadiran
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        student_id = request.form['student_id']
        date = request.form['date']
        status = request.form['status']
        add_attendance(student_id, date, status)
        return redirect('/attendance')
    attendance = get_attendance()
    students = get_students()
    return render_template('attendance.html', attendance=attendance, students=students)

@app.route('/download_attendance')
def download_attendance():
    attendance = get_attendance()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Nama Siswa', 'Tanggal', 'Status'])
    for record in attendance:
        writer.writerow(record)
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=attendance.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

# Halaman Peminjaman Perpustakaan
@app.route('/library_loans', methods=['GET', 'POST'])
def library_loans():
    if request.method == 'POST':
        student_id = request.form['student_id']
        book_title = request.form['book_title']
        loan_date = request.form['loan_date']
        add_library_loan(student_id, book_title, loan_date)
        return redirect('/library_loans')
    loans = get_library_loans()
    students = get_students()
    return render_template('library_loans.html', loans=loans, students=students)

@app.route('/download_library_loans')
def download_library_loans():
    loans = get_library_loans()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Nama Siswa', 'Judul Buku', 'Tanggal Peminjaman', 'Tanggal Pengembalian'])
    for loan in loans:
        writer.writerow(loan)
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=library_loans.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

# Halaman Kelas
@app.route('/classes', methods=['GET', 'POST'])
def classes():
    classes = get_classes()
    if request.method == 'POST':
        class_name = request.form['class_name']
        add_class(class_name)
        return redirect('/classes')
    return render_template('classes.html', classes=classes)

if __name__ == '__main__':
    app.run(debug=True)