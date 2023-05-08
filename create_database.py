import sqlite3

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        user_type TEXT NOT NULL,
        time_remaining INTEGER
    );
    """)

    cursor.execute("INSERT INTO users (username, password, user_type, time_remaining) VALUES ('employee', 'password', 'Employee', 86400)")
    cursor.execute("INSERT INTO users (username, password, user_type, time_remaining) VALUES ('customer', 'password', 'Customer', 86400)")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()