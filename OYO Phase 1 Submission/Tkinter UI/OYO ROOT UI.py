import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Assume these functions are imported from their respective files
from Login_Admin import login_admin
from Login_Users import login_user
from Database_connect import *
from mysql.connector import Error
from Tkinter_Review_UI import ReviewApp

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OYO Hotel Management System - Login")
        self.root.geometry("800x600")  # Increased size for better background display

        self.create_widgets()

    def create_widgets(self):
        # Load the background image for the login screen
        bg_image = Image.open("OYO MAIN WINDOW.jpg")  
        bg_image = bg_image.resize((800, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a label with the background image
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame = ttk.Frame(self.root, padding="20", style="Transparent.TFrame")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Configure style for transparent frame
        style = ttk.Style()
        style.configure("Transparent.TFrame", background="white")

        ttk.Button(self.frame, text="Admin Login", command=self.show_admin_login).pack(pady=10, fill="x")
        ttk.Button(self.frame, text="User Login", command=self.show_user_login).pack(pady=10, fill="x")
        ttk.Button(self.frame, text="New User", command=self.show_registration).pack(pady=10, fill="x")

    def show_admin_login(self):
        self.clear_frame()
        ttk.Label(self.frame, text="Admin Name:").pack(pady=5)
        self.admin_name_entry = ttk.Entry(self.frame)
        self.admin_name_entry.pack(pady=5)

        ttk.Label(self.frame, text="Password:").pack(pady=5)
        self.admin_password_entry = ttk.Entry(self.frame, show="*")
        self.admin_password_entry.pack(pady=5)

        ttk.Button(self.frame, text="Login", command=self.admin_login).pack(pady=10)

    def show_user_login(self):
        self.clear_frame()
        ttk.Label(self.frame, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.pack(pady=5)

        ttk.Label(self.frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(self.frame, text="Login", command=self.user_login).pack(pady=10)

    def show_registration(self):
        self.clear_frame()
        ttk.Label(self.frame, text="Username:").pack(pady=5)
        self.reg_username_entry = ttk.Entry(self.frame)
        self.reg_username_entry.pack(pady=5)

        ttk.Label(self.frame, text="Password:").pack(pady=5)
        self.reg_password_entry = ttk.Entry(self.frame, show="*")
        self.reg_password_entry.pack(pady=5)

        ttk.Label(self.frame, text="Email:").pack(pady=5)
        self.reg_email_entry = ttk.Entry(self.frame)
        self.reg_email_entry.pack(pady=5)

        ttk.Button(self.frame, text="Register", command=self.register_new_user).pack(pady=10)

    def register_new_user(self):
        user_name = self.reg_username_entry.get()
        user_password = self.reg_password_entry.get()
        email = self.reg_email_entry.get()

        result = register_user(user_name, user_password, email)
        if result == "User registered successfully":
            messagebox.showinfo("Registration Successful", "Welcome! You have been registered successfully.")
            self.show_main_window(is_admin=False)
        else:
            messagebox.showerror("Registration Failed", result)

    def admin_login(self):
        admin_name = self.admin_name_entry.get()
        password = self.admin_password_entry.get()
        result = login_admin(admin_name, password)
        if result == "Admin login successful":
            messagebox.showinfo("Login Successful", f"Welcome, Admin {admin_name}!")
            self.show_main_window(is_admin=True)
        else:
            messagebox.showerror("Login Failed", result)

    def user_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        result = login_user(username, password)
        if result == "Login successful":
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.show_main_window(is_admin=False)
        else:
            messagebox.showerror("Login Failed", result)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def show_main_window(self, is_admin):
        self.root.withdraw()  # Hide the login window
        main_window = tk.Toplevel(self.root)
        main_window.title("OYO Hotel Management System")
        main_window.geometry("800x600")
        
        def on_closing():
            self.root.destroy()  # Close the entire application
        
        main_window.protocol("WM_DELETE_WINDOW", on_closing)
        
        MainApp(main_window, is_admin)

def register_user(username, password, email):
    """
    Registers a new user.
    
    :param username: The username of the user.
    :param password: The password of the user.
    :param email: The email of the user.
    :return: Confirmation message.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Insert new user into the User table
            query = """
            INSERT INTO Users (user_name, email, user_password) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (username, email, password))
            
            # Commit the transaction
            connection.commit()
            return "User registered successfully"
        except Error as e:
            print(f"Error: {e}")
            return "Error registering the user"
        finally:
            cursor.close()
            connection.close()
    else:
        return "Connection failed"

class MainApp:
    def __init__(self, root, is_admin):
        self.root = root
        self.is_admin = is_admin
        self.create_widgets()

    def create_widgets(self):
        # Load the background image
        bg_image = Image.open("OYO HOTEL IMAGE.png")  
        bg_image = bg_image.resize((1080, 800), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a label with the background image
        bg_label = tk.Label(self.root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_photo  # Keep a reference to prevent garbage collection

        # Create a frame to hold the buttons
        button_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Configure style for transparent frame
        style = ttk.Style()
        style.configure("TFrame", background="white")

        # Create buttons for each functionality
        ttk.Button(button_frame, text="Hotel Booking System", command=self.open_hotel_booking_window).pack(pady=10, fill="x")
        ttk.Button(button_frame, text="Process Payment", command=self.open_payment_window).pack(pady=10, fill="x")
        ttk.Button(button_frame, text="Add Review", command=self.open_review_window).pack(pady=10, fill="x")

        if self.is_admin:
            ttk.Button(button_frame, text="View Records", command=self.open_records_window).pack(pady=10, fill="x")
            ttk.Button(button_frame, text="View Late Checkouts", command=self.open_fines_window).pack(pady=10, fill="x")


    def open_fines_window(self):
        from OYO_UI_for_Fines_function import display_fines
        display_fines()

    def open_hotel_booking_window(self):
        from Hotel_functions_GUI import create_and_run_gui
        create_and_run_gui()

    def open_records_window(self):
        from OYO_UI_for_retrieval_function import open_user_id_window, open_employee_id_window
        
        records_window = tk.Toplevel(self.root)
        records_window.title("View Records")
        records_window.geometry("300x200")

        button_frame = ttk.Frame(records_window, padding="20")
        button_frame.pack(expand=True, fill="both")

        ttk.Button(button_frame, text="Get User Data", command=open_user_id_window).pack(pady=10, fill="x")
        ttk.Button(button_frame, text="Get Employee Data", command=open_employee_id_window).pack(pady=10, fill="x")

    def open_payment_window(self):
        from Tkinter_Payment_UI import PaymentApp
        payment_window = tk.Toplevel(self.root)
        PaymentApp(payment_window)

    def open_review_window(self):
        from Tkinter_Review_UI import ReviewApp
        review_window = tk.Toplevel(self.root)
        ReviewApp(review_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()