import tkinter as tk  # Import the tkinter module for GUI
import ui  # Import the ui module which contains RaazEncryptApp

if __name__ == "__main__":
    # Create a Tkinter root window
    root = tk.Tk()
    
    # Create an instance of RaazEncryptApp, passing the root window as master
    app = ui.RaazEncryptApp(root)
    
    # Enter the Tkinter event loop
    root.mainloop()
