import sqlite3

# Path to SQLite database
DATABASE_PATH = "backend/Database/companies.db"

def create_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create companies table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            founders TEXT NOT NULL,
            location TEXT NOT NULL,
            capital TEXT NOT NULL,
            news TEXT
        );
    """)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database and table created successfully!")

# Run the function to create the database and table
create_db()
