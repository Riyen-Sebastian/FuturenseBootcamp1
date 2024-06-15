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
        print(f"Error: {e}")
        return None

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

# Example usage
calculate_fines_penalties("late_checkout")