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






#Function to register a new user

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

# Example usage:
# print(register_user('john_doe', 'password123', 'john@example.com'))



#Function for user login
def login_user(username, password):
    """
    Logs in a user.

    :param username: The username of the user.
    :param password: The password of the user.
    :return: Confirmation message.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Fetch the user's stored password
            query = """
            SELECT user_password FROM Users WHERE user_name = %s
            """
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                stored_password = result[0]
                # Check if the provided password matches the stored password
                if password == stored_password:
                    return "Login successful"
                else:
                    return "Invalid username or password"
            else:
                return "Invalid username or password"
        except Error as e:
            print(f"Error: {e}")
            return "Error logging in the user"
        finally:
            cursor.close()
            connection.close()
    else:
        return "Connection failed"

# Example usage:
# print(login_user('john_doe', 'password123'))


#Function for admin login
def login_admin(admin_name, password):
    """
    Logs in an admin.

    :param admin_name: The name of the admin.
    :param password: The password of the admin.
    :return: Confirmation message.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Fetch the admin's stored password
            query = """
            SELECT admin_password FROM Admins WHERE admin_name = %s
            """
            cursor.execute(query, (admin_name,))
            result = cursor.fetchone()
            if result:
                stored_password = result[0]
                # Check if the provided password matches the stored password
                if password == stored_password:
                    return "Admin login successful"
                else:
                    return "Invalid admin name or password"
            else:
                return "Invalid admin name or password"
        except Error as e:
            print(f"Error: {e}")
            return "Error logging in the admin"
        finally:
            cursor.close()
            connection.close()
    else:
        return "Connection failed"

# Example usage:
# print(login_admin('admin_user', 'admin_password123'))



#Function to update hotel details and to add hotels
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
                INSERT INTO Hotel (HotelName, City) 
                VALUES (%s, %s)
                """
                cursor.execute(query, (name, location))
                connection.commit()
                return "New hotel added successfully"
            else:
                # Update existing hotel
                query = """
                UPDATE Hotel 
                SET HotelName = %s, City  = %s 
                WHERE HotelID  = %s
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

# Example usage:
# print(update_hotel(None, 'New Hotel', 'New York'))
# print(update_hotel(1, 'Updated Hotel', 'Los Angeles'))



#Function to update room availability
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



#Function to calulate fines
def calculate_fines_penalties(query_type):
    """
    Calculates fines or penalties based on the given query type.
    """
    # Create a connection to the database
    connection = create_connection()

    # Check if the connection was successful
    if connection is None:
        print("Failed to connect to the OYO database")
        return

    try:
        cursor = connection.cursor()

        # Execute the appropriate SQL query based on the query_type
        if query_type == "late_checkout":
            query = """
                SELECT b.booking_id, h.HotelName, b.check_in, b.check_out, b.actual_checkout,
                       CASE
                           WHEN b.actual_checkout > b.check_out THEN DATEDIFF(b.actual_checkout, b.check_out) * 500
                           ELSE 0
                       END AS late_checkout_penalty
                FROM Bookings b
                JOIN Hotel h ON b.RoomID = h.HotelID
                WHERE b.actual_checkout> b.check_out;
            """
        else:
            print("Invalid query type. Please use 'late_checkout'.")
            return

        cursor.execute(query)
        results = cursor.fetchall()

        # Print the calculated fines or penalties
        for row in results:
            print(row)

    except Error as e:
        print(f"Error executing query: {e}")

    finally:
        # Close the database connection
        if connection.is_connected():
            connection.close()
            print("Connection closed")
# Example usage calculate_fines_penalties("late_checkout")


#Function to fetch customer and employee details
def retrieve_data(query_type):
    """
    Retrieves employee or user details from the OYO database.
    """
    # Create a connection to the database
    connection = create_connection()

    # Check if the connection was successful
    if connection is None:
        print("Failed to connect to the OYO database")
        return

    try:
        cursor = connection.cursor()

        # Execute the appropriate SQL query based on the query_type
        if query_type == "employees":
            query = """
                SELECT employee_id, employee_name, employee_role, contact_info
                FROM Employee
                ORDER BY employee_id;
            """
        elif query_type == "users":
            query = """
                SELECT user_name, user_id, email
                FROM users
                ORDER BY user_name ASC;
            """
        else:
            print("Invalid query type. Please use 'employees' or 'users'.")
            return

        cursor.execute(query)
        results = cursor.fetchall()

        # Print the retrieved data
        for row in results:
            print(row)

    except Error as e:
        print(f"Error executing query: {e}")

    finally:
        # Close the database connection
        if connection.is_connected():
            connection.close()
            print("Connection closed")

# Example usage
#retrieve_data("employees")
#retrieve_data("users")



#Function to add a review
def add_review(user_id, HotelID, rating, comment, complaint=None):
    """
    This function adds a review for a specific booking.

    :param user_id: The ID of the user adding the review.
    :param hotel_id: The ID of the hotel being reviewed.
    :param rating: The rating given by the user (e.g., 1 to 5 stars).
    :param comment: The comment provided by the user.
    :param complaint: Optional complaint provided by the user.
    :return: Confirmation message.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Insert the review into the Review table
            review_query = """
            INSERT INTO Review (user_id, HotelID, rating, comment, complaint) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(review_query, (user_id, HotelID, rating, comment, complaint))
            
            # Commit the transaction
            connection.commit()
            return "Review added successfully"
        except Error as e:
            print(f"Error: {e}")
            return "Error adding the review"
        finally:
            cursor.close()
            connection.close()
    else:
        return "Connection failed"

# Example usage:
# print(add_review(2, 1, 5, "Great stay!", "No complaints"))


#Function to make a payment
def process_payment(booking_id, amount):
    """
    This function processes a payment for a booking.

    :param booking_id: The ID of the booking to process payment for.
    :param amount: The amount to be paid.
    :return: Payment confirmation message.
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Step 1: Create a new payment entry in the database
            payment_query = """
            INSERT INTO Payments(booking_id, amount,payment_method) 
            VALUES (%s, %s, 'E-Wallet')
            """
            cursor.execute(payment_query, (booking_id, amount))
            
            # Step 2: Update the booking status to 'Paid'
            update_booking_query = """
            UPDATE Bookings 
            SET status = 'Paid' 
            WHERE booking_id = %s
            """
            cursor.execute(update_booking_query, (booking_id,))
            
            # Commit the transaction
            connection.commit()
            return "Payment processed successfully"
        except Error as e:
            print(f"Error: {e}")
            return "Error processing the payment"
        finally:
            cursor.close()
            connection.close()
    else:
        return "Connection failed"

# Example usage:
# print(process_payment(1, 200.00))






