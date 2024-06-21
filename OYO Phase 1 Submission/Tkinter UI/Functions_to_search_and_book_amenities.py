from Database_connect import *
#function to search for amenities
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


#function to book amenities
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

def update_hotel(hotel_id, name, location):
    """
    Updates the details of a hotel or adds a new hotel if the hotel_id is None.

    :param hotel_id: The ID of the hotel to update, or None to add a new hotel.
    :param name: The name of the hotel.
    :param location: The location of the hotel.
    :return: Confirmation message.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            if hotel_id is None:
                # Add a new hotel
                query = """
                INSERT INTO Hotel (name, location) 
                VALUES (%s, %s)
                """
                cursor.execute(query, (name, location))
                connection.commit()
                return "New hotel added successfully"
            else:
                # Update existing hotel
                query = """
                UPDATE Hotel 
                SET name = %s, location = %s 
                WHERE id = %s
                """
                cursor.execute(query, (name, location, hotel_id))
                connection.commit()
                return "Hotel updated successfully"
        except Error as e:
            print(f"Error: {e}")
            return "Error updating the hotel"
        finally:
            cursor.close()
            connection.close()
    else:
        return "Connection failed"

