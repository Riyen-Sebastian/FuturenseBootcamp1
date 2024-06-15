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
            password='Mysqlaccount1!'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

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
retrieve_data("employees")
retrieve_data("users")