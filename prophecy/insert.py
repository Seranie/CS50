from cs50 import SQL
import csv

db = SQL("sqlite:///harry.db")

with open("students.csv", "r") as file:
    students = csv.DictReader(file)
    for row in students:
        db.execute("INSERT INTO students (id, student_name) VALUES (?, ?)", row['id'], row['student_name'])
        db.execute("INSERT INTO houses (student_id, house) VALUES (?, ?)", row['id'], row['house'])
        db.execute("INSERT INTO house_assignments (student_id, head) VALUES (?, ?)", row['id'], row['head'])