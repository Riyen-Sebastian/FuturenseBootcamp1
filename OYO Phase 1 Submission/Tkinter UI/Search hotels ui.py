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
            password='mysqlpass'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

    
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

# Create the main window
root = tk.Tk()
root.title("Hotel Booking System")

# Function to search for hotels
def search_hotels_gui():
    location = location_entry.get()
    hotels = search_hotels(location)
    if hotels:
        hotel_list.delete(0, tk.END)  # Clear the previous results
        for hotel in hotels:
            hotel_list.insert(tk.END, hotel)
    else:
        messagebox.showinfo("No Hotels Found", f"No hotels found in {location}.")


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

hotel_list = tk.Listbox(hotel_list_frame, width=50, height=10)
hotel_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroll_bar = ttk.Scrollbar(hotel_list_frame, orient=tk.VERTICAL, command=hotel_list.yview)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
hotel_list.configure(yscrollcommand=scroll_bar.set)

book_button = ttk.Button(root, text="Book Selected Hotel", )
book_button.pack(pady=10)

root.mainloop()
