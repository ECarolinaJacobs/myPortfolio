import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta


# checks for missing elements in database and adds them into the database
def synch_database_json():
    con = sqlite3.connect(os.path.join(sys.path[0], "bookstore.db"))
    cursor = con.cursor()
    with open(os.path.join(sys.path[0], "books.json"), "r") as file:
        books_data = json.load(file)
    for book in books_data:
        isbn = book["isbn"]
        cursor.execute("SELECT * FROM books WHERE isbn=?", (isbn,))
        existing_book = cursor.fetchone()
        if not existing_book:
            cursor.execute(
                "INSERT INTO books (isbn, title, author, pages, year) VALUES (?, ?, ?, ?, ?)",
                (isbn, book["title"], book["author"], book["pages"], book["year"]),
            )

    con.commit()
    con.close()


# checks if book is available, if yes it returns the return date and if not it prints not available
def borrow_book():
    con = sqlite3.connect(os.path.join(sys.path[0], "bookstore.db"))
    cursor = con.cursor()
    book_id_or_isbn = input("Enter book id or isbn:")
    duration = int(input("Enter duration in days:"))
    # check if available
    cursor.execute("SELECT * FROM books WHERE id=? OR isbn=?", (book_id_or_isbn, book_id_or_isbn))
    book = cursor.fetchone()
    if book and book[6] == "AVAILABLE":
        return_date = datetime.now() + timedelta(days=duration)
        return_date_str = return_date.strftime("%d-%m-%Y")  # format the datetime object into day-month-year
        cursor.execute(
            "UPDATE books SET status=?, return_date=? WHERE id=? OR isbn=?",
            ("BORROWED", return_date_str, book[0], book[1]),
        )
        con.commit()
        con.close()
        print(return_date_str)
    else:
        con.close()
        return "book not available or wrong isbn or id"


# checks if book is returned to late if yes it calculates your fine
def return_book():
    con = sqlite3.connect(os.path.join(sys.path[0], "bookstore.db"))
    cursor = con.cursor()
    book_id_or_isbn = input("Enter book id or isbn:")
    # is book borrowed?
    cursor.execute("SELECT * FROM books WHERE id=? OR isbn=?", (book_id_or_isbn, book_id_or_isbn))
    book = cursor.fetchone()
    if book and book[6] == "BORROWED":
        return_date = datetime.strptime(book[7], "%d-%m-%Y")
        current_date = datetime.now()
        if current_date > return_date:
            days_late = (current_date - return_date).days
            payment = days_late * 0.5
            con.close()
            print("{:.2f}".format(payment))
        else:
            cursor.execute(
                "UPDATE books SET status=?, return_date=? WHERE id=? OR isbn=?", ("AVAILABLE", None, book[0], book[1])
            )
            con.commit()
            con.close()
            print("Book returned on time.")
    else:
        print("book not borrowed or wrong isbn/id")


# check is book exists based on search term
def search_book():
    con = sqlite3.connect(os.path.join(sys.path[0], "bookstore.db"))
    cursor = con.cursor()
    search_term = input("enter search term (title, isbn or author): ")
    cursor.execute(
        "SELECT * FROM books WHERE title LIKE ? OR isbn=? OR author LIKE ?",
        ("%" + search_term + "%", search_term, "%" + search_term + "%"),
    )
    books = cursor.fetchall()
    # returns book info
    if books:
        for book in books:
            status_info = "BORROWED" if book[6] == "BORROWED" else "AVAILABLE"
            print(
                {
                    "id": book[0],
                    "isbn": book[1],
                    "title": book[2],
                    "author": book[3],
                    "pages": book[4],
                    "year": book[5],
                    "status": status_info,
                    "return_date": book[7],
                }
            )
    else:
        print("Book not found.")

    con.close()


def main():
    con = sqlite3.connect(os.path.join(sys.path[0], "bookstore.db"))
    con.execute(
        """CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            pages INTEGER NOT NULL,
            year TEXT NOT NULL,
            status TEXT DEFAULT "AVAILABLE",
            return_date DATE DEFAULT NULL
        );"""
    )
    synch_database_json()
    while True:
        print("[B] Borrow book")
        print("[R] Return book")
        print("[S] Search book")
        print("[Q] Quit program")

        choice = input("Enter your choice:").upper()

        if choice == "B":
            borrow_book()
        elif choice == "R":
            return_book()
        elif choice == "S":
            search_book()
        elif choice == "Q":
            break


if __name__ == "__main__":
    main()
