import tkinter as tk
from tkinter import ttk, messagebox
import json

# Dictionary to store books
books = {}


# Load books from file
def load_books():
    global books

    try:
        with open("library.txt", "r") as file:
            books = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        books = {}


# Save books to file
def save_books():
    with open("library.txt", "w") as file:
        json.dump(books, file, indent=4)


# Display all books
def display_books():
    for row in table.get_children():
        table.delete(row)

    for isbn, book in books.items():
        table.insert("", "end", values=(
            isbn,
            book["title"],
            book["author"],
            book["quantity"]
        ))


# Clear input fields
def clear_fields():
    isbn_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)


# Add a new book
def add_book():
    isbn = isbn_entry.get().strip()
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    quantity = quantity_entry.get().strip()

    if not isbn or not title or not author or not quantity:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    if isbn in books:
        messagebox.showerror("Error", "Book already exists")
        return

    try:
        quantity = int(quantity)

        if quantity < 0:
            messagebox.showerror("Error", "Quantity cannot be negative")
            return

        books[isbn] = {
            "title": title,
            "author": author,
            "quantity": quantity
        }

        save_books()
        display_books()
        clear_fields()

        messagebox.showinfo("Success", "Book added successfully!")

    except ValueError:
        messagebox.showerror("Error", "Quantity must be a number")


# Search for a book
def search_book():
    search = search_entry.get().strip().lower()

    for row in table.get_children():
        table.delete(row)

    for isbn, book in books.items():
        if (search in isbn.lower() or
            search in book["title"].lower() or
            search in book["author"].lower()):

            table.insert("", "end", values=(
                isbn,
                book["title"],
                book["author"],
                book["quantity"]
            ))


# Borrow a book
def borrow_book():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a book")
        return

    isbn = str(table.item(selected[0], "values")[0])

    if isbn in books and books[isbn]["quantity"] > 0:
        books[isbn]["quantity"] -= 1

        save_books()
        display_books()

        messagebox.showinfo("Success", "Book borrowed successfully!")

    else:
        messagebox.showerror("Error", "No copies available")


# Return a book
def return_book():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a book")
        return

    isbn = str(table.item(selected[0], "values")[0])

    if isbn in books:
        books[isbn]["quantity"] += 1

        save_books()
        display_books()

        messagebox.showinfo("Success", "Book returned successfully!")


# Delete a book
def delete_book():
    print("Delete button clicked!")

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a book from the table first!"
        )
        return

    isbn = str(table.item(selected[0], "values")[0])

    if isbn not in books:
        messagebox.showerror("Error", "Book not found!")
        return

    confirm = messagebox.askyesno(
        "Delete Book",
        "Are you sure you want to delete this book?"
    )

    if confirm:
        del books[isbn]

        save_books()
        display_books()

        messagebox.showinfo(
            "Success",
            "Book deleted successfully!"
        )


# Display books with low stock
def low_stock():
    for row in table.get_children():
        table.delete(row)

    for isbn, book in books.items():
        if book["quantity"] < 3:
            table.insert("", "end", values=(
                isbn,
                book["title"],
                book["author"],
                book["quantity"]
            ))


# Create main window
load_books()

window = tk.Tk()
window.title("City Central Library")
window.geometry("950x650")
window.config(bg="#f0f0f0")


# Heading
heading = tk.Label(
    window,
    text="CITY CENTRAL LIBRARY",
    font=("Arial", 22, "bold"),
    bg="#f0f0f0",
    fg="#1a365d"
)
heading.pack(pady=15)


# Book information frame
input_frame = tk.LabelFrame(
    window,
    text="Book Information",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=10
)
input_frame.pack(padx=20, pady=10, fill="x")


# ISBN
tk.Label(input_frame, text="ISBN:").grid(
    row=0, column=0, padx=5, pady=5
)

isbn_entry = tk.Entry(input_frame, width=25)
isbn_entry.grid(row=0, column=1, padx=5)


# Title
tk.Label(input_frame, text="Title:").grid(
    row=0, column=2, padx=5
)

title_entry = tk.Entry(input_frame, width=25)
title_entry.grid(row=0, column=3, padx=5)


# Author
tk.Label(input_frame, text="Author:").grid(
    row=1, column=0, padx=5, pady=5
)

author_entry = tk.Entry(input_frame, width=25)
author_entry.grid(row=1, column=1, padx=5)


# Quantity
tk.Label(input_frame, text="Quantity:").grid(
    row=1, column=2, padx=5
)

quantity_entry = tk.Entry(input_frame, width=25)
quantity_entry.grid(row=1, column=3, padx=5)


# Buttons frame
button_frame = tk.Frame(window, bg="#f0f0f0")
button_frame.pack(pady=10)


# Add book button
tk.Button(
    button_frame,
    text="Add Book",
    width=14,
    bg="#287a45",
    fg="white",
    command=add_book
).grid(row=0, column=0, padx=5)


# Borrow book button
tk.Button(
    button_frame,
    text="Borrow Book",
    width=14,
    bg="#2875a5",
    fg="white",
    command=borrow_book
).grid(row=0, column=1, padx=5)


# Return book button
tk.Button(
    button_frame,
    text="Return Book",
    width=14,
    bg="#2875a5",
    fg="white",
    command=return_book
).grid(row=0, column=2, padx=5)


# Delete book button
delete_button = tk.Button(
    button_frame,
    text="Delete Book",
    width=14,
    bg="red",
    fg="white",
    command=delete_book
)

delete_button.grid(row=0, column=3, padx=5)


# Low stock button
tk.Button(
    button_frame,
    text="Low Stock",
    width=14,
    bg="#b7791f",
    fg="white",
    command=low_stock
).grid(row=0, column=4, padx=5)


# Show all books button
tk.Button(
    button_frame,
    text="Show All",
    width=14,
    command=display_books
).grid(row=0, column=5, padx=5)


# Search section
search_frame = tk.Frame(window, bg="#f0f0f0")
search_frame.pack(pady=10)

tk.Label(
    search_frame,
    text="Search Book:",
    bg="#f0f0f0",
    font=("Arial", 11)
).pack(side="left", padx=5)

search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="Search",
    command=search_book
).pack(side="left", padx=5)


# Book table
table_frame = tk.Frame(window)
table_frame.pack(padx=20, pady=10, fill="both", expand=True)

table = ttk.Treeview(
    table_frame,
    columns=("ISBN", "Title", "Author", "Quantity"),
    show="headings"
)

table.heading("ISBN", text="ISBN")
table.heading("Title", text="Book Title")
table.heading("Author", text="Author")
table.heading("Quantity", text="Quantity")

table.column("ISBN", width=150)
table.column("Title", width=250)
table.column("Author", width=250)
table.column("Quantity", width=100)

table.pack(fill="both", expand=True)


# Exit button
tk.Button(
    window,
    text="Exit",
    width=15,
    bg="#c53030",
    fg="white",
    command=lambda: [save_books(), window.destroy()]
).pack(pady=15)


# Display saved books
display_books()


# Run application
window.mainloop()