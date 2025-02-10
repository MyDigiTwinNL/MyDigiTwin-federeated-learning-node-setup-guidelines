import sqlite3
from datetime import datetime, timedelta
import random
import string

# Function to generate a random string of 12 characters
def generate_pseudoid(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to create the database and table
def create_database_and_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('testsqldata.db.sqlite')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blood_pressures (
            PARTICIPANT_PSEUDOID TEXT PRIMARY KEY,
            DATE TEXT NOT NULL,
            SYSTOLIC INTEGER NOT NULL CHECK(SYSTOLIC >= 90 AND SYSTOLIC <= 200),
            DIASTOLIC INTEGER NOT NULL CHECK(DIASTOLIC >= 50 AND DIASTOLIC <= 150)
        )
    """)
    conn.commit()
    conn.close()

# Function to insert 100 random blood pressure readings
def insert_random_readings():
    # Connect to the SQLite database
    conn = sqlite3.connect('testsqldata.db.sqlite')
    cursor = conn.cursor()

    # Generate and insert 100 random blood pressure readings
    for _ in range(100):
        participant_pseudoid = generate_pseudoid()
        date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        systolic = random.randint(90, 200)
        diastolic = random.randint(50, 150)
        
        cursor.execute("INSERT INTO blood_pressures (PARTICIPANT_PSEUDOID, DATE, SYSTOLIC, DIASTOLIC) VALUES (?,?,?,?)",
                       (participant_pseudoid, date, systolic, diastolic))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Main function to run both functions
def main():
    print("Creating database and table...")
    create_database_and_table()
    print("Database and table created.")

    print("\nInserting 100 random blood pressure readings...")
    insert_random_readings()
    print("100 random blood pressure readings inserted.")

if __name__ == "__main__":
    main()
