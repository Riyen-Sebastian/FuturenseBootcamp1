import tkinter as tk
from tkinter import messagebox

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
