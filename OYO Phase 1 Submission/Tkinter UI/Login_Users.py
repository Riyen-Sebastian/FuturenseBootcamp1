from Database_connect import *
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

# BY ARCHIE BAKSHI
