import tkinter as tk
from tkinter import messagebox
from Database_connect import *

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

class ReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Add Review")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="User ID").grid(row=0, column=0)
        self.user_id_entry = tk.Entry(self.root)
        self.user_id_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Hotel ID").grid(row=1, column=0)
        self.hotel_id_entry = tk.Entry(self.root)
        self.hotel_id_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Rating").grid(row=2, column=0)
        self.rating_entry = tk.Entry(self.root)
        self.rating_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Comment").grid(row=3, column=0)
        self.comment_entry = tk.Entry(self.root)
        self.comment_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Complaint (optional)").grid(row=4, column=0)
        self.complaint_entry = tk.Entry(self.root)
        self.complaint_entry.grid(row=4, column=1)

        self.submit_button = tk.Button(self.root, text="Submit Review", command=self.submit_review)
        self.submit_button.grid(row=5, column=0, columnspan=2)

    def submit_review(self):
        user_id = self.user_id_entry.get()
        hotel_id = self.hotel_id_entry.get()
        rating = self.rating_entry.get()
        comment = self.comment_entry.get()
        complaint = self.complaint_entry.get()

        if user_id and hotel_id and rating and comment:
            result = add_review(user_id, hotel_id, rating, comment, complaint)
            messagebox.showinfo("Result", result)
        else:
            messagebox.showwarning("Input Error", "All fields except complaint are required")
    
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ReviewApp(root)
    root.mainloop()
