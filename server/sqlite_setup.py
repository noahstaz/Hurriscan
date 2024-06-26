import os
import sqlite3
import csv
from werkzeug.security import generate_password_hash, check_password_hash

def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Data;")
    cursor.execute("DROP TABLE IF EXISTS Alert;")
    cursor.execute("DROP TABLE IF EXISTS User;")
    cursor.execute("DROP TABLE IF EXISTS Alerts;")
    cursor.execute("DROP TABLE IF EXISTS Account;")
    cursor.execute("DROP TABLE IF EXISTS user;")
    cursor.execute("DROP TABLE IF EXISTS new_table;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Data (
            obs INTEGER NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            date INTEGER NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            zon_winds REAL NOT NULL,
            mer_winds REAL NOT NULL,
            humidity REAL NOT NULL,
            air REAL NOT NULL,
            temp REAL NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Alert ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            date DATE NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            username TEXT NOT NULL,
            firstName TEXT DEFAULT "",
            lastName TEXT DEFAULT "",
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT DEFAULT "",
            zone varchar(4) DEFAULT "West",
            alerts_email TINYINT(1) DEFAULT 0,
            alerts_phone TINYINT(1) DEFAULT 0,
            isAdmin TINYINT(1) DEFAULT 0
        );
    ''')

    conn.commit()

def import_csv_to_table(conn, csv_file_path):
    cursor = conn.cursor()

    try:
        with open(csv_file_path, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            # Skip the header row
            next(csv_reader, None)

            # Insert data into the table
            for row in csv_reader:
                cursor.execute('''
                    INSERT INTO Data
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                ''', row)
                
        conn.commit()
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"Error: {e}")
        
def create_users(conn):
    cursor = conn.cursor()
    
    hashed_password = generate_password_hash("Password1", method="pbkdf2:sha256")

    cursor.execute(" INSERT INTO User (username, password, email, isAdmin) VALUES (?, ?, ?, ?)", ("Admin1", hashed_password, "Admin@gmail.com", 1))


    cursor.execute(" INSERT INTO User (username, password, email, zone, isAdmin) VALUES (?, ?, ?, ?, ?)", ("User1", hashed_password, "User@gmail.com", "West", 0))

    
    conn.commit()

def main():
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    DB_NAME = 'routing/hurriscan.db'


    

    conn = sqlite3.connect(os.path.join(basedir, DB_NAME))

    csv_file_path = '../data/cleaned_data.csv'

    create_table(conn)

    import_csv_to_table(conn, csv_file_path)

    create_users(conn)

    conn.commit()

    cursor = conn.cursor()

    print("\nTotal rows in the Data table:")
    cursor.execute("SELECT COUNT(*) FROM Data;")
    total_rows = cursor.fetchall()
    for row in total_rows:
        print(row[0])

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\nTables:")
    for table in tables:
        print(table[0])

    print("\nUsers:")
    cursor.execute("SELECT * FROM User;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    main()