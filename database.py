import sqlite3  # Importing module to work with SQLite databases
import time  # Importing module to work with time predefined function

def connect_db():
    # Connecting to SQLite database with a timeout to handle locked database scenarios
    return sqlite3.connect('encrypted_messages.db', timeout=5)

def setup_database():
    conn = None
    while conn is None:
        try:
            conn = connect_db()  # Attempt to connect to the database
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                time.sleep(1)  # Waiting for 1 second if database is locked, then retry
            else:
                raise e  # Raise exception if error is not related to a locked database
    
    cursor = conn.cursor()  # Creating a cursor object to execute SQL commands

    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    """  # SQL command to create a table for users

    create_messages_table = """
    CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        shift_key INTEGER NOT NULL,
        read_status BOOLEAN NOT NULL DEFAULT 0,
        self_destruct_time TIMESTAMP,
        FOREIGN KEY (sender_id) REFERENCES users(user_id),
        FOREIGN KEY (receiver_id) REFERENCES users(user_id)
    );
    """  # SQL command to create a table for messages

    create_notifications_table = """
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (message_id) REFERENCES messages(message_id)
    );
    """  # SQL command to create a table for notifications

    cursor.execute(create_users_table)  # Execute SQL command to create users table
    cursor.execute(create_messages_table)  # Execute SQL command to create messages table
    cursor.execute(create_notifications_table)  # Execute SQL command to create notifications table

    conn.commit()  # Commit changes to the database
    conn.close()  # Close the database connection

if __name__ == "__main__":
    setup_database()  # Call the setup_database function when the script is run directly
