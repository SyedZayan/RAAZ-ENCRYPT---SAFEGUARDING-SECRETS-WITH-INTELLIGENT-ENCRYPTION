from database import connect_db  # Importing the database connection function
from tkinter import messagebox  # Here we are Importing messagebox for displaying alerts
from encryption import deleteAllUnreadMessages  # Importing the function to delete messages

def register_user(username, password):
    if not username or not password:  # Checking if username or password is empty
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return
    db = connect_db()  # Connection to the database
    cursor = db.cursor()  # Creating a cursor object
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))  # Checking if username already exists
    if cursor.fetchone():  # If username exists, it shows an show error
        messagebox.showerror("Error", "Username already exists.")
        db.close()  
        return
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))  # Insert new user
    db.commit()  # Commit changes
    db.close()  # Close the database connection
    messagebox.showinfo("Success", "Registered successfully!")  # Show success message

def login_user(username, password):
    db = connect_db()  # Connect to the database
    cursor = db.cursor()  # Create a cursor object
    print("In Login")
    cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))  # Check credentials
    user_id = cursor.fetchone()  # Fetch user ID
    db.close()  # Close the database connection

    if user_id:  # If login info correct 
        messagebox.showinfo("Success", "Logged in successfully!")  
        return user_id[0]  # Return user ID
    else:  # If credentials are incorrect
        messagebox.showerror("Error", "Invalid username or password.")  
        return None
