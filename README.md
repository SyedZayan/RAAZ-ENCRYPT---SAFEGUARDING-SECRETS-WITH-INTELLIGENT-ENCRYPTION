# Raaz Encrypt- Safeguarding Secrets with Intelligent Encryption 
 

## Overview
Raaz Encrypt is a secure messaging application developed as part of our Bachelor of Science in Computer Science (BSCS) program at the University of Karachi. The app uses the Caesar cipher for message encryption, ensuring that only registered users with the correct decryption key can access the original messages. This project was created with a focus on simplicity, security, and ease of use.

## Project Information
- **Program**: BSCS, University of Karachi
- **Supervisor**: Sir Tauseef Mubeen
- **Group Leader**: Syed Zayan Ali ([zayanali2003@gmail.com](mailto:zayanali2003@gmail.com))
- **Team Members**:
  - Yahya Arif Butt
  - Anas Shoaib
  - Hamza Wahaj

## Features
- **User Authentication**: The app ensures that only registered users can log in and use its features. User credentials are securely stored in an SQLite database.
- **Message Encryption**: Messages are encrypted using the Caesar cipher, a simple yet effective encryption technique.
- **Message Decryption**: Users can decrypt messages by entering the correct decryption key, revealing the original message.
- **Secure Data Storage**: All user data and encrypted messages are stored securely in a local SQLite database (`encrypted_messages.db`).

## Project Structure

### File Descriptions:
- **app.py**: This is the main file that runs the entire application. It integrates all the components and starts the user interface.
- **auth.py**: Handles user registration and login processes, ensuring secure access to the application.
- **database.py**: Manages the SQLite database where user information and encrypted messages are stored.
- **encrypted_messages.db**: The database file that securely stores all data, including user credentials and encrypted messages.
- **messages.py**: Contains the logic for encrypting and decrypting messages using the Caesar cipher.
- **RAAZENCRYPT.jpg, RAAZENCRYPT.png, RAAZENCRYPT2.jpg**: Image files that are likely used in the application's user interface to enhance visual appeal.
- **ui.py**: Manages the user interface (UI), ensuring that the app is easy to navigate and use.
- **__init__.py**: Initializes the project as a Python package.

### Required Libraries:
To run Raaz Encrypt, you need to install the following Python libraries:

- **tkinter**: For creating the graphical user interface (GUI).
- **sqlite3**: For interacting with the SQLite database (built-in with Python, no need to install separately).

You can install any additional required libraries using pip:

```bash
pip install tkinter
