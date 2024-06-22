from Database_connect import *

def update_hotel(hotel_id, name, address, city, state, country, zipcode, phone):
    """
    Updates the details of a hotel or adds a new hotel with the provided hotel_id.

    :param hotel_id: The ID of the hotel to update or add.
    :param name: The name of the hotel.
    :param address: The address of the hotel.
    :param city: The city where the hotel is located.
    :param state: The state where the hotel is located.
    :param country: The country where the hotel is located.
    :param zipcode: The zip code of the hotel's location.
    :param phone: The phone number of the hotel.
    :return: Confirmation message.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Check if the hotel with the given ID exists
            check_query = "SELECT * FROM Hotel WHERE HotelID = %s"
            cursor.execute(check_query, (hotel_id,))
            existing_hotel = cursor.fetchone()

            if existing_hotel:
                # Update existing hotel
                query = """
                UPDATE Hotel 
                SET HotelName = %s, HotelAddress = %s, City = %s, State = %s, Country = %s, ZipCode = %s, PhoneNumber = %s
                WHERE HotelID = %s
                """
                cursor.execute(query, (name, address, city, state, country, zipcode, phone, hotel_id))
                connection.commit()
                return "Hotel updated successfully"
            else:
                # Add a new hotel with the provided ID
                query = """
                INSERT INTO Hotel (HotelID, HotelName, HotelAddress, City, State, Country, ZipCode, PhoneNumber) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (hotel_id, name, address, city, state, country, zipcode, phone))
                connection.commit()
                return "New hotel added successfully"
        except Error as e:
            print(f"Error: {e}")
            return f"Error updating/adding the hotel: {e}"
        finally:
            cursor.close()
            connection.close()
    else:
        return "Connection failed"