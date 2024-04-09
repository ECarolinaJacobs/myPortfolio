import os
import sys
import sqlite3


def add_student(con):
    first_name = input("Enter first name:")
    last_name = input("Enter last name:")
    city = input("Enter city:")
    date_of_birth = input("Enter date of birth:")
    classroom = input("Enter class: (optional, to skip press enter)")

    cursor = con.cursor()
    cursor.execute(
        """INSERT INTO students (first_name, last_name, city, date_of_birth, class)
           VALUES (?, ?, ?, ?, ?)""",
        (first_name, last_name, city, date_of_birth, classroom),
    )
    con.commit()
    student_number = cursor.lastrowid  # autocreates student number
    print(f"Student added with student number: {student_number}")


def assign_student_class(con):
    student_number = input("Enter student number: ")
    classroom = input("Enter class to assign: ")

    cursor = con.cursor()
    cursor.execute("""UPDATE students SET class = ? WHERE studentnumber = ?""", (classroom, student_number))
    if cursor.rowcount == 0:
        print(f"Could not find student with number: {student_number}")
    else:
        con.commit()
        print("Student assigned to class.")


def list_all_students(con):
    cursor = con.cursor()
    cursor.execute("""SELECT * FROM students ORDER BY class DESC""")
    students = cursor.fetchall()  # returns in tuples
    for student in students:
        print(student)


def list_students_class(con):
    class_name = input("Enter class to search students in: ")
    cursor = con.cursor()
    cursor.execute("""SELECT * FROM students WHERE class = ? ORDER BY studentnumber ASC""", (class_name,))
    students = cursor.fetchall()
    for student in students:
        print(student)


def search_student(con):
    search_term = input("Enter search term: ")
    cursor = con.cursor()
    cursor.execute(
        """
        SELECT * FROM students
        WHERE first_name LIKE ? OR last_name LIKE ? OR city LIKE ?
        ORDER BY studentnumber ASC LIMIT 1
    """,
        ("%" + search_term + "%", "%" + search_term + "%", "%" + search_term + "%"),
    )
    student = cursor.fetchone()
    if student:
        print(student)
    else:
        print("No matching student found.")


def main():
    con = sqlite3.connect(os.path.join(sys.path[0], "studentdatabase.db"))
    con.execute(
        """CREATE TABLE IF NOT EXISTS students (
            studentnumber INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            city TEXT NOT NULL,
            date_of_birth DATE NOT NULL,
            class TEXT DEFAULT NULL
        );"""
    )
    # menu
    while True:
        print("\nMenu:")
        print("[A] Add new student")
        print("[C] Assign student to class")
        print("[D] List all students")
        print("[L] List all students in class")
        print("[S] Search student")
        print("[Q] Quit program")

        choice = input("Choice: ").upper()

        if choice == "A":
            add_student(con)
        elif choice == "C":
            assign_student_class(con)
        elif choice == "D":
            list_all_students(con)
        elif choice == "L":
            list_students_class(con)
        elif choice == "S":
            search_student(con)
        elif choice == "Q":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
