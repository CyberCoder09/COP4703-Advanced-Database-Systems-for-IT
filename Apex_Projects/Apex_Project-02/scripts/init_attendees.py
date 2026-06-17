import os       # Importing os to read environment variables from the .env file
import psycopg2 # Importing psycopg2 to allow Python to connect to PostgreSQL

# Getting environmental parameters to connect & return connection to PostgreSQL
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

# Sample attendee data for Apex events
attendees = [
    ("Williams Roy", "williams@example.com", "VIP"),
    ("Johnson Smith", "johnson@example.com", "General"),
    ("Davis Welsh", "davis@example.com", "Speaker"),
    ("Pri Miller", "pri@example.com", "General")
]

# Exception handling
try:
    # Open a database connection using context manager, the with statement automatically closes the connection when finished
    with get_connection() as conn:
        
        # Creating cursor using context managers to execute SQL commands
        with conn.cursor() as cur:
            # Creates "attendees" table if it already does not exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS attendees(
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    ticket_type TEXT NOT NULL                  
                );
            """)

            # Insert data safely (No SQL Injection Attacks)
            # The %s placeholders keep the query safe from SQL injection
            insert_query = """
                INSERT INTO attendees (name, email, ticket_type)
                VALUES (%s, %s, %s)
                ON CONFLICT (email) DO NOTHING;
            """

            # Runs the same safe query for every attendee to insert into the database
            cur.executemany(insert_query, attendees)
            
            # Commit changes to ensure data persistence
            conn.commit()

            # Select all rows from the table
            cur.execute("SELECT * FROM attendees;")
            
            # Fetches all selected rows
            rows = cur.fetchall()

            print("\n=========================================")
            print("Apex Events Attendee Database Initialized")
            print("=========================================")
            print("Current attendees:")
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | Ticket: {row[3]}")
            print("=========================================\n")

except Exception as e:
    print(f"An error occurred during database initialization: {e}")