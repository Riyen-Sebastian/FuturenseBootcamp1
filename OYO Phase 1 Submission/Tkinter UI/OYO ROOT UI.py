import tkinter as tk
from tkinter import ttk

# Create the main root window
root = tk.Tk()
root.title("OYO Hotel Management System")
root.geometry("400x300")

def open_fines_window():
    from OYO_UI_for_Fines_function import display_fines
    display_fines()

def open_hotel_booking_window():
    from Hotel_Searching_Booking_Amenity_Searching_booking_comprehensive_UI_and_backend_Riyen import create_hotel_booking_window
    create_hotel_booking_window()

def open_records_window():
    from OYO_UI_for_retrieval_function import open_user_id_window, open_employee_id_window
    
    records_window = tk.Toplevel(root)
    records_window.title("View Records")
    records_window.geometry("300x200")

    button_frame = ttk.Frame(records_window, padding="20")
    button_frame.pack(expand=True, fill="both")

    user_data_button = ttk.Button(button_frame, text="Get User Data", command=open_user_id_window)
    user_data_button.pack(pady=10, fill="x")

    employee_data_button = ttk.Button(button_frame, text="Get Employee Data", command=open_employee_id_window)
    employee_data_button.pack(pady=10, fill="x")

# Function to create and show the main window
def show_main_window():
    # Create a frame to hold the buttons
    button_frame = ttk.Frame(root, padding="20")
    button_frame.pack(expand=True, fill="both")

    # Create buttons for each functionality in the new order
    hotel_booking_button = ttk.Button(button_frame, text="Hotel Booking System", command=open_hotel_booking_window)
    hotel_booking_button.pack(pady=10, fill="x")

    records_button = ttk.Button(button_frame, text="View Records", command=open_records_window)
    records_button.pack(pady=10, fill="x")

    fines_button = ttk.Button(button_frame, text="View Late Checkouts", command=open_fines_window)
    fines_button.pack(pady=10, fill="x")

# Schedule the main window to appear after the root is fully initialized
root.after(0, show_main_window)

# Start the main event loop
root.mainloop()