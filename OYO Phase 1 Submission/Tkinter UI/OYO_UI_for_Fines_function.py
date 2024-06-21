import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from datetime import datetime

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
        print(f"Error connecting to the database: {e}")
        return None

def calculate_late_checkout_fines():
    """
    Calculates fines for late checkouts and returns the results.
    """
    # Create a connection to the database
    connection = create_connection()

    # Check if the connection was successful
    if connection is None:
        print("Failed to connect to the OYO database")
        return []

    try:
        cursor = connection.cursor()

        # Execute the SQL query to calculate fines for late checkouts
        query = """
            SELECT b.booking_id, h.HotelName, b.check_in, b.check_out, b.actual_checkout,
                   CASE
                       WHEN b.actual_checkout > b.check_out THEN DATEDIFF(b.actual_checkout, b.check_out)
                       ELSE 0
                   END AS late_days,
                   CASE
                       WHEN b.actual_checkout > b.check_out THEN DATEDIFF(b.actual_checkout, b.check_out) * 500
                       ELSE 0
                   END AS fine
            FROM Bookings b
            JOIN Hotel h ON b.RoomID = h.HotelID
            WHERE b.actual_checkout > b.check_out;
        """

        cursor.execute(query)
        results = cursor.fetchall()

    except Error as e:
        print(f"Error executing query: {e}")
        results = []

    finally:
        # Close the database connection
        if connection.is_connected():
            connection.close()
            print("Connection closed")

    return results

def display_fines():
    # Retrieve the late checkout fines
    fines = calculate_late_checkout_fines()

    # Create a new window
    window = tk.Toplevel(root)
    window.title("Late Checkout Fines")

    # Create a treeview to display the fines
    tree = ttk.Treeview(window, columns=("booking_id", "hotel_name", "check_in", "check_out", "actual_checkout", "late_days", "fine"), show="headings")

    # Define column headings
    tree.heading("booking_id", text="Booking ID")
    tree.heading("hotel_name", text="Hotel Name")
    tree.heading("check_in", text="Check-in")
    tree.heading("check_out", text="Check-out")
    tree.heading("actual_checkout", text="Actual Checkout")
    tree.heading("late_days", text="Late Days")
    tree.heading("fine", text="Fine")

    # Insert the fines data into the treeview
    for row in fines:
        tree.insert("", "end", values=row)

    # Configure column widths
    tree.column("booking_id", width=100, anchor="center")
    tree.column("hotel_name", width=200, anchor="w")
    tree.column("check_in", width=100, anchor="center")
    tree.column("check_out", width=100, anchor="center")
    tree.column("actual_checkout", width=100, anchor="center")
    tree.column("late_days", width=100, anchor="center")
    tree.column("fine", width=100, anchor="center")

    tree.pack(pady=20)

# Create the main window
root = tk.Tk()
root.title("OYO Hotel Management System")

# Create a button to display the fines
button = tk.Button(root, text="View Late Checkout Fines", command=display_fines)
button.pack(pady=20)

root.mainloop()