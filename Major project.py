class Student:
    def __init__(self, name, roll_number):
        self.name = name
        self.roll_number = roll_number
        self.grades = {}

    def add_grade(self, subject, grade):
        if 0 <= grade <= 100:  # Ensure valid grade input
            self.grades[subject] = grade
        else:
            print(f"Invalid grade: {grade}. It must be between 0 and 100.")

    def calculate_average(self):
        if self.grades:
            return sum(self.grades.values()) / len(self.grades)
        return 0

    def display_details(self):
        print(f"Student Name: {self.name}, Roll Number: {self.roll_number}")
        print("Grades:")
        for subject, grade in self.grades.items():
            print(f"{subject}: {grade}")
        print(f"Average Grade: {self.calculate_average():.2f}")
class StudentTracker:
    def __init__(self):
        self.students = {}

    def add_student(self, name, roll_number):
        if roll_number not in self.students:
            self.students[roll_number] = Student(name, roll_number)
        else:
            print(f"Student with roll number {roll_number} already exists.")

    def add_grades(self, roll_number, subject, grade):
        student = self.students.get(roll_number)
        if student:
            student.add_grade(subject, grade)
        else:
            print(f"Student with roll number {roll_number} not found.")

    def view_student_details(self, roll_number):
        student = self.students.get(roll_number)
        if student:
            student.display_details()
        else:
            print(f"Student with roll number {roll_number} not found.")

    def calculate_class_average(self, subject):
        total_grade, count = 0, 0
        for student in self.students.values():
            if subject in student.grades:
                total_grade += student.grades[subject]
                count += 1
        if count > 0:
            return total_grade / count
        return None

    def subject_topper(self, subject):
        top_student, max_grade = None, -1
        for student in self.students.values():
            if subject in student.grades and student.grades[subject] > max_grade:
                max_grade = student.grades[subject]
                top_student = student
        return top_student
def add_student_interface(tracker):
    name = input("Enter student name: ")
    roll_number = input("Enter student roll number: ")
    tracker.add_student(name, roll_number)

def add_grade_interface(tracker):
    roll_number = input("Enter student roll number: ")
    subject = input("Enter subject name: ")
    grade = int(input("Enter grade (0-100): "))
    tracker.add_grades(roll_number, subject, grade)

def view_student_interface(tracker):
    roll_number = input("Enter student roll number: ")
    tracker.view_student_details(roll_number)

def class_average_interface(tracker):
    subject = input("Enter subject name: ")
    average = tracker.calculate_class_average(subject)
    if average is not None:
        print(f"Class average for {subject}: {average:.2f}")
    else:
        print(f"No grades found for {subject}.")

def subject_topper_interface(tracker):
    subject = input("Enter subject name: ")
    topper = tracker.subject_topper(subject)
    if topper:
        print(f"Topper in {subject}: {topper.name} with grade {topper.grades[subject]}")
    else:
        print(f"No grades found for {subject}.")

def main_menu():
    tracker = StudentTracker()
    while True:
        print("\n1. Add Student\n2. Add Grade\n3. View Student Details\n4. Calculate Class Average\n5. Find Subject Topper\n6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_student_interface(tracker)
        elif choice == '2':
            add_grade_interface(tracker)
        elif choice == '3':
            view_student_interface(tracker)
        elif choice == '4':
            class_average_interface(tracker)
        elif choice == '5':
            subject_topper_interface(tracker)
        elif choice == '6':
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
import sqlite3

class Database:
    def __init__(self, db_name="students.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS students (
                roll_number TEXT PRIMARY KEY,
                name TEXT
            )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS grades (
                roll_number TEXT,
                subject TEXT,
                grade INTEGER,
                FOREIGN KEY (roll_number) REFERENCES students(roll_number)
            )''')

    def add_student(self, student):
        with self.conn:
            self.conn.execute('INSERT INTO students (roll_number, name) VALUES (?, ?)', 
                              (student.roll_number, student.name))

    def add_grade(self, roll_number, subject, grade):
        with self.conn:
            self.conn.execute('INSERT INTO grades (roll_number, subject, grade) VALUES (?, ?, ?)', 
                              (roll_number, subject, grade))

    def fetch_student(self, roll_number):
        cur = self.conn.cursor()
        cur.execute('SELECT name FROM students WHERE roll_number = ?', (roll_number,))
        return cur.fetchone()

    def fetch_grades(self, roll_number):
        cur = self.conn.cursor()
        cur.execute('SELECT subject, grade FROM grades WHERE roll_number = ?', (roll_number,))
        return cur.fetchall()

    def close(self):
        self.conn.close()
from flask import Flask, request, render_template

app = Flask(__name__)
student_tracker = StudentTracker()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        student_tracker.add_student(name, roll_number)
        return "Student added successfully"
    return render_template('add_student.html')

@app.route('/add_grade', methods=['GET', 'POST'])
def add_grade():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        subject = request.form['subject']
        grade = int(request.form['grade'])
        student_tracker.add_grades(roll_number, subject, grade)
        return "Grade added successfully"
    return render_template('add_grade.html')

@app.route('/view_student', methods=['GET', 'POST'])
def view_student():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        student = student_tracker.view_student_details(roll_number)
        return student
    return render_template('view_student.html')

if __name__ == '__main__':
    app.run(debug=True)
def save_data_locally(tracker, filename="students_backup.txt"):
    with open(filename, "w") as file:
        for student in tracker.students.values():
            file.write(f"{student.roll_number}, {student.name}, {student.grades}\n")