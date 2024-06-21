from Database_connect import *
#function to search for hotels
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
            query = "SELECT * FROM Hotel WHERE location = %s"
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




#function to book a hotel
def book_room(user_id, room_id, check_in_date, check_out_date):
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
                INSERT INTO Booking (user_id, room_id, check_in_date, check_out_date, booking_status) 
                VALUES (%s, %s, %s, %s, 'Confirmed')
                """
                cursor.execute(booking_query, (user_id, room_id, check_in_date, check_out_date))
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
    
    
def get_available_rooms(hotel_id):
    """
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
            cursor.execute(query, (hotel_id,))
            available_rooms = cursor.fetchall()
            return available_rooms
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    else:
        return []