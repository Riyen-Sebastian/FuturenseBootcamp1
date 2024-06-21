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
            INSERT INTO Users (username, email, user_password) 
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
