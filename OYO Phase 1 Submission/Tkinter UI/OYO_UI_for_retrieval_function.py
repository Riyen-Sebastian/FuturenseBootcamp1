import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Creates and returns a connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='OYO',
            user='root',
            password='Mysqlaccount1!'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def retrieve_user_data():
    """
    Retrieves user details from the OYO database based on the input user ID.
    """
    user_id = user_id_entry.get()

    # Create a connection to the database
    connection = create_connection()

    # Check if the connection was successful
    if connection is None:
        print("Failed to connect to the OYO database")
        return

    try:
        cursor = connection.cursor()

        query = """
            SELECT user_name, user_id, email
            FROM users
            WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        # Open a new window to display the user data
        user_data_window = tk.Toplevel(root)
        user_data_window.title("User Data")

        # Create a treeview to display the retrieved data
        tree = ttk.Treeview(user_data_window)
        tree.pack(pady=10)

        # Configure column headings for user data
        tree["columns"] = ("user_name", "user_id", "email")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("user_name", anchor="w", width=120)
        tree.column("user_id", anchor="w", width=100)
        tree.column("email", anchor="w", width=200)

        tree.heading("#0", text="", anchor="w")
        tree.heading("user_name", text="User Name", anchor="w")
        tree.heading("user_id", text="User ID", anchor="w")
        tree.heading("email", text="Email", anchor="w")

        # Insert the retrieved data into the treeview
        if result:
            tree.insert("", "end", values=result)
        else:
            tree.insert("", "end", values=("No user found with the given ID",))

    except Error as e:
        print(f"Error executing query: {e}")

    finally:
        # Close the database connection
        if connection.is_connected():
            connection.close()
            print("Connection closed")

    # Close the user ID entry window
    user_id_window.destroy()

def retrieve_employee_data():
    """
    Retrieves employee details from the OYO database based on the input employee ID.
    """
    employee_id = employee_id_entry.get()

    # Create a connection to the database
    connection = create_connection()

    # Check if the connection was successful
    if connection is None:
        print("Failed to connect to the OYO database")
        return

    try:
        cursor = connection.cursor()

        query = """
            SELECT employee_id, employee_name, employee_role, contact_info
            FROM Employee
            WHERE employee_id = %s
        """
        cursor.execute(query, (employee_id,))
        result = cursor.fetchone()

        # Open a new window to display the employee data
        employee_data_window = tk.Toplevel(root)
        employee_data_window.title("Employee Data")

        # Create a treeview to display the retrieved data
        tree = ttk.Treeview(employee_data_window)
        tree.pack(pady=10)

        # Configure column headings for employee data
        tree["columns"] = ("employee_id", "employee_name", "employee_role", "contact_info")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("employee_id", anchor="w", width=100)
        tree.column("employee_name", anchor="w", width=150)
        tree.column("employee_role", anchor="w", width=120)
        tree.column("contact_info", anchor="w", width=150)

        tree.heading("#0", text="", anchor="w")
        tree.heading("employee_id", text="Employee ID", anchor="w")
        tree.heading("employee_name", text="Employee Name", anchor="w")
        tree.heading("employee_role", text="Employee Role", anchor="w")
        tree.heading("contact_info", text="Contact Info", anchor="w")

        # Insert the retrieved data into the treeview
        if result:
            tree.insert("", "end", values=result)
        else:
            tree.insert("", "end", values=("No employee found with the given ID",))

    except Error as e:
        print(f"Error executing query: {e}")

    finally:
        # Close the database connection
        if connection.is_connected():
            connection.close()
            print("Connection closed")

    # Close the employee ID entry window
    employee_id_window.destroy()

def open_user_id_window():
    """
    Opens a window to enter the user ID.
    """
    global user_id_window, user_id_entry

    user_id_window = tk.Toplevel(root)
    user_id_window.title("Enter User ID")

    user_id_label = tk.Label(user_id_window, text="User ID:")
    user_id_label.pack(pady=5)

    user_id_entry = tk.Entry(user_id_window)
    user_id_entry.pack(pady=5)

    submit_button = tk.Button(user_id_window, text="Submit", command=retrieve_user_data)
    submit_button.pack(pady=5)

def open_employee_id_window():
    """
    Opens a window to enter the employee ID.
    """
    global employee_id_window, employee_id_entry

    employee_id_window = tk.Toplevel(root)
    employee_id_window.title("Enter Employee ID")

    employee_id_label = tk.Label(employee_id_window, text="Employee ID:")
    employee_id_label.pack(pady=5)

    employee_id_entry = tk.Entry(employee_id_window)
    employee_id_entry.pack(pady=5)

    submit_button = tk.Button(employee_id_window, text="Submit", command=retrieve_employee_data)
    submit_button.pack(pady=5)

# Create the main window
root = tk.Tk()
root.title("OYO Database")

# Create buttons to open sub-windows for user and employee ID input
user_button = tk.Button(root, text="Get User Data", command=open_user_id_window)
user_button.pack(pady=5)

employee_button = tk.Button(root, text="Get Employee Data", command=open_employee_id_window)
employee_button.pack(pady=5)

# Start the main event loop
root.mainloop()