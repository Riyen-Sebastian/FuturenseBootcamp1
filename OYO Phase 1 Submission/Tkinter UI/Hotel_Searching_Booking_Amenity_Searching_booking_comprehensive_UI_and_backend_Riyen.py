import mysql.connector
from mysql.connector import Error

from Database_connect import *


#Function to search for Hotels by City
def search_hotels(location):
    """
    Searches for hotels in a given location.

    :param location: The location to search hotels in.
    :return: List of hotels in the given location.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM Hotel WHERE city = %s"
            cursor.execute(query, (location,))
            hotels = cursor.fetchall()
            return hotels
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    else:
        return []


# Example usage:
# print(search_hotels('New York'))




#Function to book a room
def book_room(booking_id,user_id, room_id, check_in_date, check_out_date):
    """
    Books a room for a user if it is available.

    :param user_id: The ID of the user making the booking.
    :param room_id: The ID of the room to be booked.
    :param check_in_date: The desired check-in date.
    :param check_out_date: The desired check-out date.
    :return: Confirmation message or booking ID.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Check room availability
            availability_query = """
            SELECT COUNT(*) FROM Bookings 
            WHERE RoomID = %s AND 
            (%s BETWEEN check_in AND check_out 
            OR %s BETWEEN check_in AND check_out
            OR check_in BETWEEN %s AND %s 
            OR check_out BETWEEN %s AND %s)
            """
            cursor.execute(availability_query, (room_id, check_in_date, check_out_date, check_in_date, check_out_date, check_in_date, check_out_date))
            count = cursor.fetchone()[0]
            if count == 0:
                # Room is available, proceed to book
                booking_query = """
                INSERT INTO Bookings (booking_id,user_id, RoomID, check_in, check_out, status) 
                VALUES (%s,%s, %s, %s, %s, 'Confirmed')
                """
                cursor.execute(booking_query, (booking_id,user_id, room_id, check_in_date, check_out_date))
                connection.commit()
                return "Room booked successfully"
            else:
                return "Room not available"
        except Error as e:
            print(f"Error: {e}")
            return "Error booking the room"
        finally:
            cursor.close()
            connection.close()
    else:
        return "Connection failed"

# Example usage:
# print(book_room(6,1, 101, '2024-07-01', '2024-07-10'))


#Function to search for available amenities by hotel
def view_amenities(hotel_id):
    """
    Retrieves all amenities offered by a specific hotel.

    :param hotel_id: The ID of the hotel to view amenities for.
    :return: List of amenities offered by the hotel.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM Service WHERE HotelID = %s"
            cursor.execute(query, (hotel_id,))
            amenities = cursor.fetchall()
            return amenities
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    else:
        return []

# Example usage:
# print(view_amenities(1))


#Function to book amenity
def book_amenity(user_id, service_id, booking_id=None):
    """
    Allows a user to book an amenity offered by the hotel, either during booking or during their stay.

    :param user_id: The ID of the user availing the service.
    :param service_id: The ID of the service to be availed.
    :param booking_id: Optional booking ID if the service is availed during the booking process.
    :return: Confirmation message.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Service_Avail (user_id, service_id, booking_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, service_id, booking_id))
            connection.commit()
            return "Service booked successfully"
        except Error as e:
            print(f"Error: {e}")
            return "Error booking the service"
        finally:
            cursor.close()
            connection.close()
    else:
        return "Connection failed"

# Example usage:
# print(book_amenity(1, 1, 1))







import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Create the main window
root = tk.Tk()
root.title("Hotel Booking System")


# Function to search for hotels and display available rooms
def search_hotels_gui():
    location = location_entry.get()
    hotels = search_hotels(location)
    if hotels:
        hotel_list.delete(0, tk.END)  # Clear the previous results
        for hotel in hotels:
            hotel_list.insert(tk.END, hotel)
    else:
        messagebox.showinfo("No Hotels Found", f"No hotels found in {location}.")
        
def get_available_rooms(hotel_id):
    """d
    Retrieves a list of available rooms for a specific hotel.
    :param hotel_id: The ID of the hotel to get available rooms for.
    :return: List of available room IDs and room types.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT RoomID, RoomType
                FROM Rooms
                WHERE HotelID = %s AND IsAvailable = 1
            """
            print(f"Executing query: {query}")
            print(f"With hotel_id: {hotel_id}")
            cursor.execute(query, (hotel_id,))
            available_rooms = cursor.fetchall()
            print(f"Query result: {available_rooms}")
            return available_rooms
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
                print("Database connection closed.")
    else:
        return []        

# Function to proceed to the booking page
def book_hotel():
    selected_hotel = hotel_list.curselection()
    if selected_hotel:
        hotel_id = hotel_list.get(selected_hotel)[0]  # Assuming the hotel ID is the first field in the tuple
        available_rooms= get_available_rooms(hotel_id)
        booking_window = tk.Toplevel(root)
        booking_window.title("Book Hotel")
        booking_window.grab_set()  # Make the booking window modal

               
        room_frame = ttk.Frame(booking_window, padding=10)
        room_frame.pack(pady=10)
        booking_id_label = ttk.Label(room_frame, text=f"Available Rooms: {available_rooms}")
        booking_id_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        # Add booking form widgets
        booking_form_frame = ttk.Frame(booking_window, padding=10)
        booking_form_frame.pack(pady=10)

        booking_id_label = ttk.Label(booking_form_frame, text="Booking ID:")
        booking_id_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        booking_id_entry = ttk.Entry(booking_form_frame)
        booking_id_entry.grid(row=0, column=1, padx=5, pady=5)

        user_id_label = ttk.Label(booking_form_frame, text="User ID:")
        user_id_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        user_id_entry = ttk.Entry(booking_form_frame)
        user_id_entry.grid(row=1, column=1, padx=5, pady=5)

        check_in_label = ttk.Label(booking_form_frame, text="Check-In Date:")
        check_in_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        check_in_entry = ttk.Entry(booking_form_frame)
        check_in_entry.grid(row=2, column=1, padx=5, pady=5)

        check_out_label = ttk.Label(booking_form_frame, text="Check-Out Date:")
        check_out_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        check_out_entry = ttk.Entry(booking_form_frame)
        check_out_entry.grid(row=3, column=1, padx=5, pady=5)


        RoomID_label = ttk.Label(booking_form_frame, text="Room ID:")
        RoomID_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        RoomID_entry = ttk.Entry(booking_form_frame)
        RoomID_entry.grid(row=4, column=1, padx=5, pady=5)

        

        # Example booking function
        def book_room_gui():
            user_id = user_id_entry.get()
            check_in_date = check_in_entry.get()
            check_out_date = check_out_entry.get()
            room_id = RoomID_entry.get()  # Assuming a room ID of 101 for demonstration purposes
            booking_id = booking_id_entry.get()  # Assuming a booking ID of 1 for demonstration purposes

            # Validate input
            if not user_id or not check_in_date or not check_out_date or not room_id or not booking_id:
                messagebox.showerror("Invalid Input", "Please provide all the required information.")
                return

            # Validate check-in and check-out dates
            try:
                check_in_date = datetime.datetime.strptime(check_in_date, "%Y-%m-%d").date()
                check_out_date = datetime.datetime.strptime(check_out_date, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Invalid Date Format", "Please enter the dates in the format YYYY-MM-DD.")
                return

            if check_out_date <= check_in_date:
                messagebox.showerror("Invalid Date Range", "Check-out date must be after check-in date.")
                return

            result = book_room(booking_id, int(user_id), room_id, check_in_date.isoformat(), check_out_date.isoformat())
            messagebox.showinfo("Booking Result", result)

        book_button = tk.Button(booking_form_frame, text="Book Room", command=book_room_gui)
        book_button.grid(row=5, column=1, padx=5, pady=5, sticky=tk.E)

        # Function to search for amenities
        def search_amenities_gui():
            amenities = view_amenities(hotel_id)
            if amenities:
                amenity_list.delete(0, tk.END)  # Clear the previous results
                for amenity in amenities:
                    amenity_list.insert(tk.END, amenity)
            else:
                messagebox.showinfo("No Amenities Found", "No amenities found for this hotel.")

        # Function to book an amenity
        def book_amenity_gui():
            selected_amenity = amenity_list.curselection()
            if selected_amenity:
                service_id = amenity_list.get(selected_amenity)[0]  # Assuming the service ID is the first field in the tuple
                result = book_amenity(int(user_id_entry.get()), service_id, booking_id_entry.get())
                messagebox.showinfo("Booking Result", result)
            else:
                messagebox.showwarning("No Amenity Selected", "Please select an amenity from the list.")

        # Create the amenities frame
        amenities_frame = ttk.Frame(booking_window, padding=10)
        amenities_frame.pack(pady=10)

        amenities_label = ttk.Label(amenities_frame, text="Amenities:")
        amenities_label.pack(side=tk.TOP, pady=5)

        amenity_list = tk.Listbox(amenities_frame, width=50, height=5)
        amenity_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_bar = ttk.Scrollbar(amenities_frame, orient=tk.VERTICAL, command=amenity_list.yview)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        amenity_list.configure(yscrollcommand=scroll_bar.set)

        search_amenities_button = ttk.Button(amenities_frame, text="Search Amenities", command=search_amenities_gui)
        search_amenities_button.pack(side=tk.TOP, pady=5)

        book_amenity_button = ttk.Button(amenities_frame, text="Book Selected Amenity", command=book_amenity_gui)
        book_amenity_button.pack(side=tk.TOP, pady=5)

    else:
        messagebox.showwarning("No Hotel Selected", "Please select a hotel from the list.")

# Create the search frame
search_frame = ttk.Frame(root, padding=10)
search_frame.pack(pady=10)

location_label = ttk.Label(search_frame, text="Enter Location:")
location_label.pack(side=tk.LEFT, padx=5)

location_entry = ttk.Entry(search_frame)
location_entry.pack(side=tk.LEFT, padx=5)


search_button = ttk.Button(search_frame, text="Search Hotels", command=search_hotels_gui)
search_button.pack(side=tk.LEFT, padx=5)

# Create the hotel list frame
hotel_list_frame = ttk.Frame(root, padding=10)
hotel_list_frame.pack(pady=10)

hotel_list_label = ttk.Label(hotel_list_frame, text="Hotel List:")
hotel_list_label.pack(side=tk.TOP, pady=5)

hotel_list = tk.Listbox(hotel_list_frame, width=80, height=10)
hotel_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroll_bar = ttk.Scrollbar(hotel_list_frame, orient=tk.VERTICAL, command=hotel_list.yview)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
hotel_list.configure(yscrollcommand=scroll_bar.set)

book_button = ttk.Button(root, text="Book Selected Hotel", command=book_hotel)
book_button.pack(pady=10)

root.mainloop()
