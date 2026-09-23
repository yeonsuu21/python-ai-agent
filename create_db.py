import sqlite3


connection = sqlite3.connect("data/employee.db")

cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """
)

employees = [
    ("김연수", "yeonsu@example.com"),
    ("박철수", "chulsu@example.com"),
    ("이영희", "younghee@example.com"),
]

cursor.executemany(
    """
    INSERT INTO employees (name, email)
    VALUES (?, ?)
    """,
    employees
)

connection.commit()
connection.close()

print("employee.db 생성 완료")