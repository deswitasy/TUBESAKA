import time
from tkinter import Tk, Label, Entry, Button, Text

# Dummy data: list of dictionaries with ID and balance
customers = [
    {"id": i, "balance": (i % 10 + 1) * 100000} for i in range(101, 201)
]

# Recursive search function
def search_customer_recursive(customers, id, index=0):
    if index >= len(customers):
        return None
    if customers[index]['id'] == id:
        return customers[index]
    return search_customer_recursive(customers, id, index + 1)

# Iterative search function
def search_customer_iterative(customers, id):
    for customer in customers:
        if customer['id'] == id:
            return customer
    return None

# Function to process withdrawal
def process_withdrawal(id, amount, output_box):
    start_recursive = time.perf_counter()
    customer_recursive = search_customer_recursive(customers, id)
    end_recursive = time.perf_counter()

    start_iterative = time.perf_counter()
    customer_iterative = search_customer_iterative(customers, id)
    end_iterative = time.perf_counter()

    output_box.delete(1.0, "end")

    if not customer_recursive:
        output_box.insert("end", f"Error: ID {id} tidak ditemukan.\n")
        return

    if customer_recursive['balance'] < amount:
        output_box.insert("end", "Error: Saldo tidak mencukupi untuk penarikan.\n")
        return

    # Deduct balance
    customer_recursive['balance'] -= amount
    output_box.insert("end", f"Sukses: Penarikan sebesar {amount} berhasil. Saldo tersisa: {customer_recursive['balance']}\n")

    # Show running times in ms
    recursive_time_ms = (end_recursive - start_recursive) * 1000
    iterative_time_ms = (end_iterative - start_iterative) * 1000
    output_box.insert("end", f"Waktu Pencarian (Recursive): {recursive_time_ms:.3f} ms\n")
    output_box.insert("end", f"Waktu Pencarian (Iterative): {iterative_time_ms:.3f} ms\n")

# Setup UI
def setup_ui():
    def on_submit():
        try:
            id = int(entry_id.get())
            amount = int(entry_amount.get())
            process_withdrawal(id, amount, output_box)
        except ValueError:
            output_box.delete(1.0, "end")
            output_box.insert("end", "Error: Input tidak valid. Pastikan ID dan jumlah penarikan adalah angka.\n")

    # Root window
    root = Tk()
    root.title("Bank Balance Checker")

    # Labels and entries
    Label(root, text="ID Nasabah:").grid(row=0, column=0, padx=10, pady=5)
    entry_id = Entry(root)
    entry_id.grid(row=0, column=1, padx=10, pady=5)

    Label(root, text="Jumlah Penarikan:").grid(row=1, column=0, padx=10, pady=5)
    entry_amount = Entry(root)
    entry_amount.grid(row=1, column=1, padx=10, pady=5)

    # Submit button
    Button(root, text="Submit", command=on_submit).grid(row=2, column=0, columnspan=2, pady=10)

    # Output box
    Label(root, text="Output:").grid(row=3, column=0, columnspan=2)
    output_box = Text(root, height=10, width=50)
    output_box.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    root.mainloop()

# Run the UI
if __name__ == "__main__":
    setup_ui()
