from database import connect_db  # Import the function to connect to the database
from datetime import datetime, timedelta  # Import datetime utilities
from tkinter import messagebox  # Import message box utilities for user interaction

def encrypt_message(sender_id, receiver_id, message, shift_key, self_destruct_minutes):
    db = connect_db()  # Connect to the database
    cursor = db.cursor()  # Create a cursor object
    # Encrypt message using Caesar cipher logic
    encrypted_message = ''.join(
        chr((ord(char) - 97 + shift_key) % 26 + 97) if char.islower() else
        chr((ord(char) - 65 + shift_key) % 26 + 65) if char.isupper() else char
        for char in message
    )
    # Calculate self destruct time for the message
    self_destruct_time = datetime.now() + timedelta(minutes=self_destruct_minutes) if self_destruct_minutes else None
    print(datetime.now())  # Print current time
    # Insert encrypted message into the database
    cursor.execute("INSERT INTO messages (sender_id, receiver_id, message, shift_key, self_destruct_time) VALUES (?, ?, ?, ?, ?)", 
                   (sender_id, receiver_id, encrypted_message, shift_key, self_destruct_time))
    db.commit()  # Commit changes to the database
    db.close()  # Close database connection
    messagebox.showinfo("Success", "Message encrypted and sent.")  # Inform user of success

def decrypt_message(user_id, message_id, shift_key):
    db = connect_db()  # Connect to the database
    cursor = db.cursor()  # Create a cursor object
    # Retrieve encrypted message from the database
    cursor.execute("SELECT message, shift_key, read_status FROM messages WHERE message_id = ? AND receiver_id = ?", (message_id, user_id))
    row = cursor.fetchone()  # Fetch the results
    if not row:
        messagebox.showerror("Error", "Message not found or you don't have permission to access it.")  # Show error if no message found
        db.close()  # Close database connection
        return None
    encrypted_message, stored_shift_key, read_status = row
    if shift_key != stored_shift_key:
        db.close()  # Close database connection if shift key does not match
        return None
    # Decrypt the message using the reverse of the encryption logic
    decrypted_message = ''.join(
        chr((ord(char) - 97 - shift_key) % 26 + 97) if char.islower() else
        chr((ord(char) - 65 - shift_key) % 26 + 65) if char.isupper() else char
        for char in encrypted_message
    )
    cursor.execute("UPDATE messages SET read_status = 1 WHERE message_id = ?", (message_id,))  # Update read status
    db.commit()  # Commit changes to the database
    db.close()  # Close database connection
    return decrypted_message  # Return the decrypted message

def delete_message(message_id):
    db = connect_db()  # Connect to the database
    cursor = db.cursor()  # Create a cursor object
    cursor.execute("DELETE FROM messages WHERE message_id = ?", (message_id,))  # Delete the specified message
    db.commit()  # Commit changes to the database
    db.close()  # Close database connection

def get_users():
    db = connect_db()  # Connect to the database
    cursor = db.cursor()  # Create a cursor object
    cursor.execute("SELECT user_id, username FROM users")  # Retrieve all users
    users = cursor.fetchall()  # Fetch all results
    db.close()  # Close database connection
    return users  # Return list of users

def get_received_messages(user_id):
    db = connect_db()  # Connect to the database
    cursor = db.cursor()  # Create a cursor object
    cursor.execute("SELECT message_id, sender_id, message, read_status FROM messages WHERE receiver_id = ?", (user_id,))  # Retrieve received messages
    messages = cursor.fetchall()  # Fetch all results
    db.close()  # Close database connection
    return messages  # Return list of messages

def get_username(user_id):
    db = connect_db()  # Connect to the database
    cursor = db.cursor()  # Create a cursor object
    cursor.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))  # Retrieve username
    username = cursor.fetchone()[0]  # Fetch the result
    db.close()  # Close database connection
    return username  # Return the username

def get_notifications(user_id):
    db = connect_db()  # Connect to the database
    cursor = db.cursor()  # Create a cursor object
    cursor.execute("SELECT message_id FROM notifications WHERE user_id = ?", (user_id,))  # Retrieve notifications for the user
    notifications = cursor.fetchall()  # Fetch all results
    db.close()  # Close database connection
    return [notification[0] for notification in notifications]  # Return list of notification message IDs

def delete_notification(user_id):
    db = connect_db()  # Connect to the database
    cursor = db.cursor()  # Create a cursor object
    cursor.execute("DELETE FROM notifications WHERE user_id = ?", (user_id,))  # Delete notifications for the user
    db.commit()  # Commit changes to the database
    db.close()  # Close database connection

def deleteAllUnreadMessages():
    db = connect_db()  # Connect to the database
    cursor = db.cursor()  # Create a cursor object
    print("Ready to Delete All")
    # Deleting all messages with passed self-destruct time
    cursor.execute("DELETE FROM messages WHERE read_status = 1 AND self_destruct_time <= ?", (datetime.now(),))
    db.commit()  # Commit changes to the database
    db.close()  # Close database connection
    #self.populate_inbox()
