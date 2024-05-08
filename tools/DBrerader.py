import sqlite3
from datetime import datetime

def db_init():
    try:
        conn = sqlite3.connect('PeopleCollection.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AllData (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100),
                surname VARCHAR(100),
                age INT,
                born_year INT,
                nicknames VARCHAR(255),
                emails VARCHAR(255),
                leaked_passwords TEXT,
                address TEXT,
                last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print('> Initialization passed')
    except sqlite3.Error as e:
        print("> SQLite Error during initialization:", e)
    finally:
        if conn:
            conn.close()

def read_sqlite_database(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()
        for table in table_names:
            table_name = table[0]
            print(f"Table: {table_name}")
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            print("Columns:", column_names)
            cursor.execute(f"SELECT * FROM {table_name};")
            records = cursor.fetchall()
            for record in records:
                print(record)
            print()
    except sqlite3.Error as e:
        print("SQLite Error during reading:", e)
    finally:
        if conn:
            conn.close()
            
def add_record():
    try:
        # Use a context manager to open the database connection
        with sqlite3.connect('PeopleCollection.db') as conn:
            cursor = conn.cursor()

            # Get user input
            name = input("> Enter name (mandatory): ")
            surname = input("> Enter surname (mandatory): ")
            born_year_input = input("> Enter year of birth (leave blank if unknown): ")
            born_year = int(born_year_input) if born_year_input else None

            # Calculate age based on born_year if available
            if born_year:
                current_year = datetime.now().year
                age = current_year - born_year
            else:
                age = None

            # Check if at least name or surname is provided
            if not name.strip() and not surname.strip():
                print("> Error: At least name or surname must be provided.")
                return

            # Get input for other fields
            nicknames = input("> Enter nicknames (comma separated if multiple): ")
            emails = input("> Enter emails (comma separated if multiple): ")
            leaked_passwords = input("> Enter leaked passwords (if any): ")
            address = input("> Enter address: ")

            # Insert record into database
            cursor.execute("""
                INSERT INTO AllData (name, surname, age, born_year, nicknames, emails, leaked_passwords, address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, surname, age, born_year, nicknames, emails, leaked_passwords, address))

            conn.commit()
            print("> Record added successfully!")

    except sqlite3.Error as e:
        print("> SQLite Error during record addition:", e)
            
if __name__ == "__main__":
    db_init()
    db_file_path = "PeopleCollection.db"
    # read_sqlite_database(db_file_path)
    add_record()
