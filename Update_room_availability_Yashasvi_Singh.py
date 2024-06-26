
from Database_connect import *
def update_room_availability(room_id, availability):
    """
    Updates the availability of a room.

    :param room_id: The ID of the room to update.
    :param availability: The new availability status (e.g., 'Available', 'Not Available').
    :return: Confirmation message.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            UPDATE Rooms 
            SET IsAvailable = %s 
            WHERE RoomID = %s
            """
            cursor.execute(query, (availability, room_id))
            connection.commit()
            return "Room availability updated successfully"
        except Error as e:
            print(f"Error: {e}")
            return "Error updating room availability"
        finally:
            cursor.close()
            connection.close()
    else:
        return "Connection failed"

# Example usage:
# print(update_room_availability(101, 1))
# print(update_room_availability(102, 0))
