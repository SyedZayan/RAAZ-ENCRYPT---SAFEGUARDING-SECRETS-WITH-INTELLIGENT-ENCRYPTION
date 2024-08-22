import tkinter as tk
from tkinter import ttk, messagebox
from auth import register_user, login_user
from encryption import encrypt_message, decrypt_message, get_users, get_received_messages, delete_message, get_notifications, delete_notification, deleteAllUnreadMessages
import time
from datetime import datetime, timedelta
import threading
from PIL import Image, ImageTk
import sqlite3

def connect_db():
    return sqlite3.connect('encrypted_messages.db')  # Connecting to the SQLite database

class RaazEncryptApp:
    def __init__(self, root):
        self.root = root  # Reference to the main Tkinter window
        self.root.title("RaazEncrypt - Safeguarding Secrets with Intelligent Encryption")  # window title
        self.root.geometry('800x600')  # Setting the zsize of the window
        self.user_id = None  # User ID for the currently logged-in user

        # Loading and setting up background image
        self.background_image = Image.open('RAAZENCRYPT.jpg')  # BG image
        screen_width = self.root.winfo_screenwidth()  # Get screen width
        screen_height = self.root.winfo_screenheight()  # Get screen height
        self.root.geometry(f"{screen_width}x{screen_height}")  # AdjustINg window size to full screen
        self.background_image = self.background_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Resize the image to fit the screen
        self.bg_image = ImageTk.PhotoImage(self.background_image)  # Create a PhotoImage object
        self.background_label = tk.Label(self.root, image=self.bg_image)  # Create a label to display the background
        self.background_label.place(relwidth=1, relheight=1)  # Place the label to cover the entire window

        # Styling for the GUI elements
        style = ttk.Style()
        style.configure("TLabel", foreground="#000", background="#F0F0F0", font=("Sitka Heading", 12))
        style.configure("TButton", foreground="#1e1e1e", background="#00cc66", font=("Sitka Heading", 12, "bold"))
        style.configure("TEntry", foreground="#000000", background="#FFFFFF", font=("Sitka Heading", 22))
        style.configure("TCombobox", foreground="#000000", background="#FFFFFF", font=("Sitka Heading", 12))
        style.configure("Treeview", background="#333333", foreground="#d6d6d6", fieldbackground="#333333", font=("Sitka Heading", 12))
        style.map('Treeview', background=[('selected', '#00cc66')])

        # Frames for different sections of the GUI
        self.frame_login = ttk.Frame(root, padding="20 20 20 20", style="TFrame")
        self.frame_login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.frame_register = ttk.Frame(root, padding="20 20 20 20", style="TFrame")
        self.frame_register.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.frame_main = ttk.Frame(root, padding="20 20 20 20", style="TFrame")
        self.frame_main.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.create_login_frame()  # Creating and displaying the login frame

    def create_login_frame(self):
        # Login frame setup
        self.clear_frames()  # Clear any existing frames
        self.frame_login.tkraise()  # Raise the login frame to the top
        #Labels and entry fields for username and password
        ttk.Label(self.frame_login, text="SIGN IN", font=("Sitka Heading", 30, "bold")).grid(row=0, column=1, pady=5, sticky='w')
        ttk.Label(self.frame_login, text="Username: ", font=("Sitka Heading",)).grid(row=1, column=0, pady=10)
        ttk.Label(self.frame_login, text="Password: ", font=("Sitka Heading",)).grid(row=2, column=0, pady=10)
        self.login_username = ttk.Entry(self.frame_login, width=30)
        self.login_password = ttk.Entry(self.frame_login, show="*", width=30)
        self.login_username.grid(row=1, column=1, pady=10)
        self.login_password.grid(row=2, column=1, pady=10)

        # Checkbox to show/hide password
        self.show_password_var = tk.BooleanVar()
        self.show_password_check = ttk.Checkbutton(self.frame_login, text="Show Password", variable=self.show_password_var, command=self.toggle_password)
        self.show_password_check.grid(row=3, column=1, pady=5, sticky='w')

        # Buttons for login and signup
        ttk.Button(self.frame_login, text="Login", command=self.handle_login).grid(row=4, column=1, pady=5, sticky='w')
        ttk.Button(self.frame_login, text="Signup", command=self.create_register_frame).grid(row=5, column=1, pady=5, sticky='w')
        self.frame_login.pack(expand=True)  # Pack the frame to make it visible

    def toggle_password(self):
        # Toggle the visibility of the password
        if self.show_password_var.get():
            self.login_password.config(show="")
        else:
            self.login_password.config(show="*")

    def create_register_frame(self):
        # Registration frame setup
        self.clear_frames()  # Clear any existing frames
        self.frame_register.tkraise()  # Raise the register frame to the top
        # Create labels and entry fields for username and password registration
        ttk.Label(self.frame_register, text="SIGN UP", font=("Sitka Heading", 30, "bold")).grid(row=0, column=1, pady=5, sticky='w')
        ttk.Label(self.frame_register, text="Username: ").grid(row=1, column=0, pady=10)
        ttk.Label(self.frame_register, text="Password: ").grid(row=2, column=0, pady=10)
        self.register_username = ttk.Entry(self.frame_register, width=30)
        self.register_password = ttk.Entry(self.frame_register, show="*", width=30)
        self.register_username.grid(row=1, column=1, pady=10)
        self.register_password.grid(row=2, column=1, pady=10)

        # Checkbox to show/hide password
        self.show_register_password_var = tk.BooleanVar()
        self.show_register_password_check = ttk.Checkbutton(self.frame_register, text="Show Password", variable=self.show_register_password_var, command=self.toggle_register_password)
        self.show_register_password_check.grid(row=3, column=1, pady=5, sticky='w')

        # Buttons for registration and returning to login
        ttk.Button(self.frame_register, text="Register", command=self.handle_register).grid(row=4, column=1, pady=5, sticky='w')
        ttk.Button(self.frame_register, text="Back to Login", command=self.create_login_frame).grid(row=5, column=1, pady=5, sticky='w')
        self.frame_register.pack(expand=True)  # Pack the frame to make it visible

    def toggle_register_password(self):
        # Toggle the visibility of the registration password
        if self.show_register_password_var.get():
            self.register_password.config(show="")
        else:
            self.register_password.config(show="*")

    def create_main_frame(self):
        # Main application frame setup after successful login
        self.clear_frames()  # Clear any existing frames
        self.frame_main.tkraise()  # Raise the main frame to the top
        users = get_users()  # Retrieve list of users
        user_dict = {username: user_id for user_id, username in users}  # Map usernames to user IDs for selection

        # Display Welcome Message
        username = self.get_username(self.user_id)  # Get the username of the logged-in user
        welcome_message = f"Welcome to the RaazEncrypt, {username}!"  # Construct welcome message
        ttk.Label(self.frame_main, text=welcome_message, font=("Sitka Heading", 20, "bold")).grid(row=0, column=1, padx=0, pady=0)

        # Setup for sending messages
        ttk.Label(self.frame_main, text="Send Message", font=("Sitka Heading", 20, "bold")).grid(row=1, column=1, pady=10)
        ttk.Label(self.frame_main, text="Select User: ").grid(row=2, column=0, pady=5)
        ttk.Label(self.frame_main, text="Message: ").grid(row=3, column=0, pady=5)
        ttk.Label(self.frame_main, text="Shift Key: ").grid(row=4, column=0, pady=5)
        ttk.Label(self.frame_main, text="Self-Destruct (minutes): ").grid(row=5, column=0, pady=5)

        # Entry fields for sending messages
        self.user_combobox = ttk.Combobox(self.frame_main, values=list(user_dict.keys()), width=30)
        self.message_entry = ttk.Entry(self.frame_main, width=30)
        self.shift_key_entry = ttk.Entry(self.frame_main, width=30)
        self.self_destruct_entry = ttk.Entry(self.frame_main, width=30)

        # Layout the entry fields in the grid
        self.user_combobox.grid(row=2, column=1)
        self.message_entry.grid(row=3, column=1)
        self.shift_key_entry.grid(row=4, column=1, pady=5)
        self.self_destruct_entry.grid(row=5, column=1, pady=5)

        # Button to send the message and logout button
        ttk.Button(self.frame_main, text="Send Message", command=lambda: self.handle_encrypt(user_dict)).grid(row=6, column=1, pady=20)
        ttk.Button(self.frame_main, text="Logout", command=self.handle_logout).grid(row=0, column=4, pady=10)

        # Setup for displaying the inbox
        ttk.Label(self.frame_main, text="Inbox", font=("Sitka Heading", 20, "bold")).grid(row=7, column=1, pady=10)
        self.inbox_tree = ttk.Treeview(self.frame_main, columns=("sender", "message", "status"), show='headings')
        self.inbox_tree.heading("sender", text="Sender")
        self.inbox_tree.heading("message", text="Message")
        self.inbox_tree.heading("status", text="Status")

        # Layout the Treeview and button to refresh inbox
        self.inbox_tree.grid(row=8, column=0, columnspan=5, pady=10)
        self.populate_inbox()
        ttk.Button(self.frame_main, text="Refresh", command=self.populate_inbox).grid(row=7, column=3, pady=10)

        # Button to display notifications
        self.notification_button = ttk.Button(self.frame_main, text="Notifications", command=self.show_notifications)
        self.notification_button.grid(row=7, column=0, pady=10)

        self.frame_main.pack(expand=True)  # Pack the main frame to make it visible

    def show_notifications(self):
        # Display notifications in a new window
        notifications = get_notifications(self.user_id)  # Retrieve notifications for the user
        notification_window = tk.Toplevel(self.root)  # Create a top-level window for notifications
        notification_window.title("Notifications")  # Set the title for the notification window
        notification_window.geometry('300x200')  # Set the size of the notification window

        if not notifications:
            tk.Label(notification_window, text="No notifications.").pack(pady=20)  # Show message if no notifications
        else:
            for msg_id in notifications:
                receiver_id = self.get_notif_rec_name(msg_id)  # Get the receiver ID for the notification
                rec_username = self.get_username(receiver_id)  # Get the username of the receiver
                tk.Label(notification_window, text=f"Your message to {rec_username} has been read.").pack(pady=10)  # Display notification message

            ttk.Button(notification_window, text="Clear Notifications", command=lambda: self.clear_notifications(notification_window)).pack(pady=10)  # Button to clear notifications

    def clear_notifications(self, notification_window):
        delete_notification(self.user_id)  # Clear all notifications for the user
        notification_window.destroy()  # Close the notification window

    def populate_inbox(self):
        deleteAllUnreadMessages()  # Delete all unread messages that meet certain conditions
        for row in self.inbox_tree.get_children():
            self.inbox_tree.delete(row)  # Clear existing entries in the Treeview

        messages = get_received_messages(self.user_id)  # Retrieve all received messages for the user
        user_dict = {user_id: username for user_id, username in get_users()}  # Map user IDs to usernames

        for msg_id, sender_id, msg, read_status in messages:
            sender_username = user_dict.get(sender_id, "Unknown")  # Get the sender's username, default to "Unknown"
            msg_status = "Read" if read_status else "Unread"  # Determine the read status of the message
            self.inbox_tree.insert("", "end", iid=msg_id, values=(sender_username, msg, msg_status))  # Insert the message into the Treeview

        self.inbox_tree.bind("<Double-1>", self.on_message_select)  # Bind double-click event to open message details

    def on_message_select(self, event):
        selected_item = self.inbox_tree.selection()[0]  # Get the selected item in the Treeview
        self.decrypt_message_prompt(selected_item)  # Prompt to decrypt the selected message

    def decrypt_message_prompt(self, message_id):
        decrypt_window = tk.Toplevel(self.root)  # Create a top-level window for decrypting the message
        decrypt_window.title("Decrypt Message")  # Set the title for the decryption window
        decrypt_window.geometry('300x200')  # Set the size of the decryption window
        tk.Label(decrypt_window, text="Enter Shift Key:").pack(pady=10)  # Label for entering the shift key
        shift_key_entry = tk.Entry(decrypt_window, show="*", width=30)  # Entry field for the shift key
        shift_key_entry.pack(pady=10)  # Pack the shift key entry field
        tk.Button(decrypt_window, text="Decrypt", command=lambda: self.handle_decrypt(message_id, shift_key_entry.get(), decrypt_window)).pack(pady=10)  # Button to initiate decryption

    def handle_decrypt(self, message_id, shift_key, decrypt_window):
        try:
            shift_key = int(shift_key)  # Convert shift key input to an integer
            message = decrypt_message(self.user_id, message_id, shift_key)  # Attempt to decrypt the message using the shift key
            if message:
                messagebox.showinfo("Decrypted Message", message)  # Show the decrypted message in a messagebox
                self.notify_sender(message_id)  # Notify the sender that the message has been read
                self.populate_inbox()  # Refresh the inbox to update message status
                print(message_id)
                threading.Thread(target=self.delete_message_after_delay(message_id), args=()).start()  # Start a thread to handle delayed message deletion
                decrypt_window.destroy()  # Close the decryption window
            else:
                messagebox.showerror("Error", "Incorrect shift key")  # Show an error if the shift key is incorrect
                delete_message(message_id)  # Delete the message
                self.handle_logout()  # Log out the user
        except ValueError:
            messagebox.showerror("Error", "Shift key must be an integer")  # Show an error if the shift key input is not an integer

    def notify_sender(self, message_id):
        sender_id = self.get_sender_id(message_id)  # Retrieve the sender ID for the message
        db = connect_db()  # Connect to the database
        cursor = db.cursor()  # Create a cursor object
        cursor.execute("INSERT INTO notifications (user_id, message_id) VALUES (?, ?)", (sender_id, message_id))  # Insert a notification record for the sender
        db.commit()  # Commit the database transaction
        db.close()  # Close the database connection

    def get_sender_id(self, message_id):
        db = connect_db()  # Connect to the database
        cursor = db.cursor()  # Create a cursor object
        cursor.execute("SELECT sender_id FROM messages WHERE message_id = ?", (message_id,))  # Retrieve the sender ID for the specified message
        result = cursor.fetchone()  # Fetch the result
        db.close()  # Close the database connection
        if result:
            return result[0]  # Return the sender ID
        return None  # Return None if no sender ID found

    def get_username(self, user_id):
        db = connect_db()  # Connect to the database
        cursor = db.cursor()  # Create a cursor object
        cursor.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))  # Retrieve the username for the specified user ID
        result = cursor.fetchone()  # Fetch the result
        db.close()  # Close the database connection
        if result:
            return result[0]  # Return the username
        return None  # Return None if no username found
    
    def get_notif_rec_name(self, msg_id):
        db = connect_db()  # Connect to the database
        cursor = db.cursor()  # Create a cursor object
        cursor.execute("SELECT receiver_id FROM messages WHERE message_id = ?", (msg_id,))  # Retrieve the receiver ID for the specified message ID
        result = cursor.fetchone()  # Fetch the result
        db.close()  # Close the database connection
        if result:
            return result[0]  # Return the receiver ID
        return None  # Return None if no receiver ID found

    def delete_message_after_delay(self, message_id):
        print("In message delay function" + message_id)  # Print a message indicating the start of the delay function
        message_id = int(message_id)  # Convert the message ID to an integer
        #time.sleep(self.get_self_destruct_time(message_id) * 60)  # Sleep for the self-destruct time converted from minutes to seconds
        #time.sleep(60)  # Sleep for 60 seconds (for demonstration)
        self.delete_message(message_id)  # Delete the message

    def get_self_destruct_time(self, message_id):
        db = connect_db()  # Connect to the database
        cursor = db.cursor()  # Create a cursor object
        cursor.execute("SELECT self_destruct_time FROM messages WHERE message_id = ?", (message_id,))  # Retrieve the self-destruct time for the specified message ID
        result = cursor.fetchone()  # Fetch the result
        db.close()  # Close the database connection
        if result and result[0]:
            return result[0]  # Return the self-destruct time
        return 0  # Return 0 if no self-destruct time is set

    def delete_message(self, message_id):
        db = connect_db()  # Connect to the database
        cursor = db.cursor()  # Create a cursor object
        print("Ready to Delete" + str(message_id))  # Print a message indicating readiness to delete
        cursor.execute("DELETE FROM messages WHERE read_status = 1 AND message_id = ? AND self_destruct_time <= ?", (message_id, datetime.now(),))  # Delete the message if the read status is 1 and the current time is past the self-destruct time
        
        db.commit()  # Commit the database transaction
        db.close()  # Close the database connection
        self.populate_inbox()  # Refresh the inbox to reflect the deletion
        
    

    def clear_frames(self):
        for frame in (self.frame_login, self.frame_register, self.frame_main):
            for widget in frame.winfo_children():
                widget.destroy()  # Destroy all widgets in the frame
            frame.pack_forget()  # Remove the frame from layout

    def handle_register(self):
        username = self.register_username.get()  # Get the username from the entry field
        password = self.register_password.get()  # Get the password from the entry field
        register_user(username, password)  # Register the user with the provided username and password
        self.create_login_frame()  # Return to the login frame after registration

    def handle_login(self):
        username = self.login_username.get()  # Get the username from the entry field
        password = self.login_password.get()  # Get the password from the entry field
        self.user_id = login_user(username, password)  # Attempt to log in with the provided credentials
        if self.user_id:
            self.create_main_frame()  # Create the main frame if login is successful

    def handle_logout(self):
        self.user_id = None  # Clear the user ID to log out the user
        self.create_login_frame()  # Return to the login frame after logout

    def handle_encrypt(self, user_dict):
        receiver_username = self.user_combobox.get()  # Get the selected receiver username from the combobox
        receiver_id = user_dict.get(receiver_username)  # Get the receiver ID from the user dictionary
        if not receiver_id:
            messagebox.showerror("Error", "Please select a valid user.")  # Show an error if the selected user is not valid
            return
        message = self.message_entry.get()  # Get the message from the entry field
        shift_key = int(self.shift_key_entry.get())  # Get the shift key from the entry field
        self_destruct_minutes = int(self.self_destruct_entry.get()) if self.self_destruct_entry.get() else None  # Get the self-destruct minutes from the entry field, if provided
        encrypt_message(self.user_id, receiver_id, message, shift_key, self_destruct_minutes)  # Encrypt and send the message
        self.clear_message_form()  # Clear the message form after sending

    def clear_message_form(self):
        self.user_combobox.set('')  # Clear the user combobox
        self.message_entry.delete(0, tk.END)  # Clear the message entry field
        self.shift_key_entry.delete(0, tk.END)  # Clear the shift key entry field
        self.self_destruct_entry.delete(0, tk.END)  # Clear the self-destruct entry field

if __name__ == "__main__":
    root = tk.Tk()  # Create the main Tkinter window
    app = RaazEncryptApp(root)  # Create an instance of the RaazEncryptApp
    root.mainloop()  # Start the Tkinter event loop
