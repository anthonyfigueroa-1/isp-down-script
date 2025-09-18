import sqlite3
from root.logger import logs

file = "/req-files/db/departments.db"
#Passing in departments from root.api.departments to cache them for quick access
def add_dep_db(departments):
    db = sqlite3.connect(file)
    cursor = db.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS departments(
                       id NUM PRIMARY KEY,
                       name TEXT)
                   """)
    db.commit()

    for department in departments:
        id = department.get("id")
        name = department.get("name")
        try:
            cursor.execute("""
                           INSERT INTO departments (id, name)
                           VALUES(?, ?)""",
                           (id, name))
            db.commit()

        except sqlite3.IntegrityError:
            continue

    cursor.close()
    db.close()

def load_dep_db():
    db = sqlite3.connect(file)
    cursor = db.cursor()

    cursor.execute("""ATTACH DATABASE departments AS departments""")

    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()

    return departments
