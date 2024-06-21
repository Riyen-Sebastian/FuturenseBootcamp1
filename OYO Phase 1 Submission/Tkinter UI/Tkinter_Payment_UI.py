import tkinter as tk
from tkinter import messagebox
from Database_connect import *

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
class PaymentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Payment")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Booking ID").grid(row=0, column=0)
        self.booking_id_entry = tk.Entry(self.root)
        self.booking_id_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Amount").grid(row=1, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1)

        self.submit_button = tk.Button(self.root, text="Process Payment", command=self.process_payment)
        self.submit_button.grid(row=2, column=0, columnspan=2)

    def process_payment(self):
        booking_id = self.booking_id_entry.get()
        amount = self.amount_entry.get()

        if booking_id and amount:
            try:
                amount = float(amount)
                result = process_payment(booking_id, amount)
                messagebox.showinfo("Result", result)
            except ValueError:
                messagebox.showwarning("Input Error", "Amount must be a number")
        else:
            messagebox.showwarning("Input Error", "Both fields are required")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaymentApp(root)
    root.mainloop()
