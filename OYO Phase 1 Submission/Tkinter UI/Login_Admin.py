from Database_connect import *

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

# BY ARCHIE BAKSHI
