import sqlite3

connection = sqlite3.connect("pdf.db")  
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS pdfs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL
)
""")

connection.commit()
connection.close()

def add_pdf_to_db(file_name):
    connection = sqlite3.connect("pdf.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO pdfs (file_name) VALUES (?)", (file_name,))
    connection.commit()
    connection.close()

def delete_pdf_from_db(file_name):
    connection = sqlite3.connect("pdf.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM pdfs WHERE file_name = ?", (file_name,))
    connection.commit()
    connection.close()
