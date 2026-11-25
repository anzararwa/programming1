import tkinter as tk
from tkinter import ttk, messagebox
import json

# ==============================
# COLOUR THEME
# ==============================

BG = "#edf2f7"
NAVY = "#172b4d"
BLUE = "#2875a5"
TEAL = "#159a9c"
GREEN = "#239b56"
RED = "#d64545"
PURPLE = "#805ad5"
ORANGE = "#d69e2e"
WHITE = "#ffffff"
DARK = "#263238"

books = {}


# ==============================
# BOOK DATA FUNCTIONS
# ==============================

def load_books():
    global books

    try:
        with open("Library.txt", "r") as file:
            books = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        books = {}


def save_books():
    with open("Library.txt", "w") as file:
        json.dump(books, file, indent=4)


# OPTIMISATION:
# This reusable function clears and fills the book table.
# It is used by display_books(), search_book() and low_stock().
def populate_table(records):
    # Clear the existing table
    for row in table.get_children():
        table.delete(row)

    # Insert the supplied book records
    for index, (isbn, book) in enumerate(records):
        tag = "evenrow" if index % 2 == 0 else "oddrow"

        table.insert(
            "",
            "end",
            values=(
                isbn,
                book["title"],
                book["author"],
                book["quantity"]
            ),
            tags=(tag,)
        )


def display_books():
    populate_table(books.items())
    update_status(f"Showing all books: {len(books)}")


def clear_fields():
    isbn_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)


def update_status(message):
    status_label.config(text=f"  {message}")


# ==============================
# ADD BOOK
# ==============================

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
            messagebox.showerror(
                "Error",
                "Quantity cannot be negative"
            )
            return

        books[isbn] = {
            "title": title,
            "author": author,
            "quantity": quantity
        }

        save_books()
        display_books()
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Book added successfully!"
        )

        update_status("New book added successfully")

    except ValueError:
        messagebox.showerror(
            "Error",
            "Quantity must be a number"
        )


# ==============================
# SEARCH BOOK
# ==============================

def search_book():
    search = search_entry.get().strip().lower()

    matching_books = []

    for isbn, book in books.items():
        if (
            search in isbn.lower()
            or search in book["title"].lower()
            or search in book["author"].lower()
        ):
            matching_books.append((isbn, book))

    # Use the reusable function to display search results
    populate_table(matching_books)

    update_status(
        f"Search results: {len(matching_books)} book(s)"
    )


# ==============================
# BORROW BOOK
# ==============================

def borrow_book():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a book"
        )
        return

    isbn = str(table.item(selected[0], "values")[0])

    if isbn in books and books[isbn]["quantity"] > 0:
        books[isbn]["quantity"] -= 1

        save_books()
        display_books()

        messagebox.showinfo(
            "Success",
            "Book borrowed successfully!"
        )

        update_status("Book borrowed successfully")

    else:
        messagebox.showerror(
            "Error",
            "No copies available"
        )


# ==============================
# RETURN BOOK
# ==============================

def return_book():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a book"
        )
        return

    isbn = str(table.item(selected[0], "values")[0])

    if isbn in books:
        books[isbn]["quantity"] += 1

        save_books()
        display_books()

        messagebox.showinfo(
            "Success",
            "Book returned successfully!"
        )

        update_status("Book returned successfully")


# ==============================
# DELETE BOOK
# ==============================

def delete_book():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a book from the table first!"
        )
        return

    isbn = str(table.item(selected[0], "values")[0])

    if isbn not in books:
        messagebox.showerror(
            "Error",
            "Book not found!"
        )
        return

    confirm = messagebox.askyesno(
        "Delete Book",
        "Are you sure you want to delete this book?"
    )

    if confirm:
        del books[isbn]

        save_books()
        display_books()
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Book deleted successfully!"
        )

        update_status("Book deleted successfully")


# ==============================
# EDIT BOOK
# ==============================

def edit_book():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a book to edit!"
        )
        return

    isbn = str(table.item(selected[0], "values")[0])

    if isbn not in books:
        messagebox.showerror(
            "Error",
            "Book not found!"
        )
        return

    book = books[isbn]

    clear_fields()

    isbn_entry.insert(0, isbn)
    title_entry.insert(0, book["title"])
    author_entry.insert(0, book["author"])
    quantity_entry.insert(0, book["quantity"])

    messagebox.showinfo(
        "Edit Book",
        "Change the details and click Update Book."
    )

    update_status("Editing selected book")


# ==============================
# UPDATE BOOK
# ==============================

def update_book():
    isbn = isbn_entry.get().strip()
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    quantity = quantity_entry.get().strip()

    if not isbn or not title or not author or not quantity:
        messagebox.showerror(
            "Error",
            "Please fill in all fields!"
        )
        return

    if isbn not in books:
        messagebox.showerror(
            "Error",
            "Book not found! Select a book using Edit Book first."
        )
        return

    try:
        quantity = int(quantity)

        if quantity < 0:
            messagebox.showerror(
                "Error",
                "Quantity cannot be negative!"
            )
            return

        books[isbn]["title"] = title
        books[isbn]["author"] = author
        books[isbn]["quantity"] = quantity

        save_books()
        display_books()
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Book updated successfully!"
        )

        update_status("Book details updated")

    except ValueError:
        messagebox.showerror(
            "Error",
            "Quantity must be a number!"
        )


# ==============================
# LOW STOCK
# ==============================

def low_stock():
    low_stock_books = []

    for isbn, book in books.items():
        if book["quantity"] < 3:
            low_stock_books.append((isbn, book))

    # Use the reusable function to display low-stock records
    populate_table(low_stock_books)

    update_status(
        f"Low stock books: {len(low_stock_books)}"
    )


def show_all():
    search_entry.delete(0, tk.END)
    display_books()


# ==============================
# BUTTON DESIGN
# ==============================

def create_button(parent, text, colour, command, width=14):
    button = tk.Button(
        parent,
        text=text,
        width=width,
        font=("Arial", 9, "bold"),
        bg=colour,
        fg=WHITE,
        activebackground=NAVY,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=3,
        pady=4,
        command=command
    )

    def on_enter(event):
        button.config(bg=NAVY)

    def on_leave(event):
        button.config(bg=colour)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return button


# ==============================
# MAIN WINDOW
# ==============================

load_books()

window = tk.Tk()

window.title("City Central Library Management System")
window.state("zoomed")
window.minsize(1000, 700)
window.config(bg=BG)


# ==============================
# HEADER
# ==============================

header = tk.Frame(
    window,
    bg=NAVY,
    height=85
)

header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="CITY CENTRAL LIBRARY",
    font=("Arial", 22, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(pady=(12, 2))

tk.Label(
    header,
    text="BOOK MANAGEMENT SYSTEM",
    font=("Arial", 10, "bold"),
    bg=NAVY,
    fg="#67e8e8"
).pack()


# ==============================
# BOOK INFORMATION PANEL
# ==============================

input_frame = tk.LabelFrame(
    window,
    text="  BOOK INFORMATION  ",
    font=("Arial", 11, "bold"),
    bg=WHITE,
    fg=NAVY,
    padx=12,
    pady=7,
    relief="groove",
    bd=2
)

input_frame.pack(
    padx=18,
    pady=5,
    fill="x"
)

label_style = {
    "font": ("Arial", 10, "bold"),
    "bg": WHITE,
    "fg": DARK
}

entry_style = {
    "font": ("Arial", 10),
    "relief": "solid",
    "bd": 1
}


# ISBN

tk.Label(
    input_frame,
    text="ISBN:",
    **label_style
).grid(row=0, column=0, padx=8, pady=5, sticky="w")

isbn_entry = tk.Entry(
    input_frame,
    width=24,
    **entry_style
)

isbn_entry.grid(
    row=0,
    column=1,
    padx=8,
    pady=5
)


# BOOK TITLE

tk.Label(
    input_frame,
    text="Book Title:",
    **label_style
).grid(row=0, column=2, padx=8, pady=5, sticky="w")

title_entry = tk.Entry(
    input_frame,
    width=24,
    **entry_style
)

title_entry.grid(
    row=0,
    column=3,
    padx=8,
    pady=5
)


# AUTHOR

tk.Label(
    input_frame,
    text="Author:",
    **label_style
).grid(row=1, column=0, padx=8, pady=5, sticky="w")

author_entry = tk.Entry(
    input_frame,
    width=24,
    **entry_style
)

author_entry.grid(
    row=1,
    column=1,
    padx=8,
    pady=5
)


# QUANTITY

tk.Label(
    input_frame,
    text="Quantity:",
    **label_style
).grid(row=1, column=2, padx=8, pady=5, sticky="w")

quantity_entry = tk.Entry(
    input_frame,
    width=24,
    **entry_style
)

quantity_entry.grid(
    row=1,
    column=3,
    padx=8,
    pady=5
)


# ==============================
# LIBRARY OPERATIONS
# ==============================

button_frame = tk.LabelFrame(
    window,
    text="  LIBRARY OPERATIONS  ",
    font=("Arial", 11, "bold"),
    bg=BG,
    fg=NAVY,
    padx=8,
    pady=6
)

button_frame.pack(
    padx=18,
    pady=5,
    fill="x"
)


buttons = [
    ("Add Book", GREEN, add_book),
    ("Borrow Book", BLUE, borrow_book),
    ("Return Book", TEAL, return_book),
    ("Delete Book", RED, delete_book),
    ("Edit Book", PURPLE, edit_book),
    ("Update Book", "#138b83", update_book),
    ("Low Stock", ORANGE, low_stock),
    ("Show All", NAVY, show_all)
]


for index, (text, colour, command) in enumerate(buttons):
    button = create_button(
        button_frame,
        text,
        colour,
        command,
        width=14
    )

    button.grid(
        row=index // 4,
        column=index % 4,
        padx=7,
        pady=5,
        sticky="ew"
    )


for column in range(4):
    button_frame.columnconfigure(column, weight=1)


# ==============================
# SEARCH PANEL
# ==============================

search_frame = tk.Frame(
    window,
    bg=BG
)

search_frame.pack(pady=5)


tk.Label(
    search_frame,
    text="SEARCH BOOK:",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=NAVY
).pack(side="left", padx=6)


search_entry = tk.Entry(
    search_frame,
    width=30,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

search_entry.pack(
    side="left",
    padx=6,
    ipady=3
)


search_button = create_button(
    search_frame,
    "Search",
    BLUE,
    search_book,
    width=12
)

search_button.pack(
    side="left",
    padx=5
)


# ==============================
# EXIT BUTTON
# ==============================

def exit_program():
    save_books()
    window.destroy()


exit_button = create_button(
    search_frame,
    "EXIT SYSTEM",
    RED,
    exit_program,
    width=14
)

exit_button.pack(
    side="left",
    padx=8
)


# ==============================
# BOOK TABLE
# ==============================

table_frame = tk.Frame(
    window,
    bg=WHITE,
    bd=2,
    relief="groove"
)

table_frame.pack(
    padx=15,
    pady=5,
    fill="both",
    expand=True
)


# TABLE STYLING

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=DARK,
    rowheight=25,
    fieldbackground=WHITE,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=NAVY,
    foreground=WHITE,
    font=("Arial", 10, "bold"),
    padding=7
)

style.map(
    "Treeview",
    background=[("selected", TEAL)],
    foreground=[("selected", WHITE)]
)


# TREEVIEW

table = ttk.Treeview(
    table_frame,
    columns=("ISBN", "Title", "Author", "Quantity"),
    show="headings",
    height=20
)


table.heading("ISBN", text="ISBN")
table.heading("Title", text="BOOK TITLE")
table.heading("Author", text="AUTHOR")
table.heading("Quantity", text="QUANTITY")


table.column(
    "ISBN",
    width=170,
    anchor="center"
)

table.column(
    "Title",
    width=350,
    anchor="w"
)

table.column(
    "Author",
    width=300,
    anchor="w"
)

table.column(
    "Quantity",
    width=120,
    anchor="center"
)


# ALTERNATING ROW COLOURS

table.tag_configure(
    "evenrow",
    background="#eaf4fb"
)

table.tag_configure(
    "oddrow",
    background=WHITE
)


# SCROLLBARS

vertical_scroll = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

horizontal_scroll = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=table.xview
)


table.configure(
    yscrollcommand=vertical_scroll.set,
    xscrollcommand=horizontal_scroll.set
)


table.grid(
    row=0,
    column=0,
    sticky="nsew"
)

vertical_scroll.grid(
    row=0,
    column=1,
    sticky="ns"
)

horizontal_scroll.grid(
    row=1,
    column=0,
    sticky="ew"
)


table_frame.rowconfigure(
    0,
    weight=1
)

table_frame.columnconfigure(
    0,
    weight=1
)


# ==============================
# STATUS BAR
# ==============================

status_label = tk.Label(
    window,
    text="  Welcome to City Central Library",
    font=("Arial", 9),
    bg="#dce6f1",
    fg=NAVY,
    anchor="w",
    padx=10,
    pady=5
)

status_label.pack(
    fill="x",
    side="bottom"
)


# ==============================
# START APPLICATION
# ==============================

display_books()

window.mainloop()
