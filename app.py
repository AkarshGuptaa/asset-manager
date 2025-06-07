import customtkinter as ctk
import tkinter.filedialog as fd
from tkinter import ttk
import pandas as pd
from io import BytesIO
import qrcode
from PIL import Image, ImageTk


CSV_FILE = "assets.csv"

df = pd.read_csv(CSV_FILE)

window = ctk.CTk()
window.geometry("800x700")
window.title("Asset Manager")

main_frame = ctk.CTkFrame(window)
view_frame = ctk.CTkFrame(window)
add_frame = ctk.CTkFrame(window)
add_row_form_frame = ctk.CTkFrame(window)
manage_columns_frame = ctk.CTkFrame(window)
manage_columns_frame.place(relwidth=1, relheight=1)

window.wm_iconbitmap("icon.ico")

def load_treeview_data(data=None):
    global df
    if data is None:
        df = pd.read_csv(CSV_FILE)
        data = df

    # Clear existing rows and columns
    for row in tree.get_children():
        tree.delete(row)

    tree["columns"] = list(data.columns)

    for col in tree["columns"]:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, anchor="center", width=120)
    tree.column("#0", width=0, stretch=False)

    for index, row in data.iterrows():
        values = tuple(row[col] for col in data.columns)
        tree.insert("", "end", iid=index, values=values)



def show_frame(frame):
    frame.tkraise()
    if frame == view_frame:
        load_treeview_data()

for frame in (main_frame, view_frame, add_frame, add_row_form_frame):
    frame.place(relwidth=1, relheight=1)

def click():
    print('view clicked')

def update_treeview(filtered_data):
    load_treeview_data(data=filtered_data)


name = ctk.CTkLabel(main_frame, text="Asset Manager", font=('Arial', 30, 'bold'))
name.pack(pady=100)

view_button = ctk.CTkButton(main_frame,
                            text="View",
                            command=lambda: show_frame(view_frame),
                            font=("Arial", 20, 'bold'),
                            height=60,
                            width=150)
view_button.pack(pady=10)

add_button = ctk.CTkButton(main_frame,
                           text="Add",
                           command=lambda: show_frame(add_frame),
                           font=("Arial", 20, 'bold'),
                           height=60,
                           width=150)
add_button.pack(pady=40)

quit_button = ctk.CTkButton(main_frame,
                            text="Quit",
                            command=window.destroy,  # closes the app
                            font=("Arial", 20, 'bold'),
                            height=60,
                            width=150)
quit_button.pack(pady=10)

back_button = ctk.CTkButton(view_frame, text="⬅ Back", font=("Arial", 16),
                            command=lambda: show_frame(main_frame))

# --- Add Frame UI ---
add_title = ctk.CTkLabel(add_frame, text="Edit Asset Details", font=('Arial', 30, 'bold'))
add_title.pack(pady=120)

add_row_button = ctk.CTkButton(add_frame, text="Add Row", font=('Arial', 20, 'bold'), width=150, height=60,
                               command=lambda: show_frame(add_row_form_frame))
add_row_button.pack(pady=20)

# Get the columns from the CSV DataFrame
columns = list(df.columns)

entries = {}  # To hold references to input fields

add_row_form_title = ctk.CTkLabel(add_row_form_frame, text="Add New Asset", font=('Arial', 24, 'bold'))
add_row_form_title.pack(pady=20)

form_frame = ctk.CTkFrame(add_row_form_frame)
form_frame.pack(pady=10, padx=20)

# Create label + entry for each column dynamically
for col in columns:
    label = ctk.CTkLabel(form_frame, text=col, anchor="w", width=150)
    label.pack(pady=5, fill='x')

    entry = ctk.CTkEntry(form_frame, width=300)
    entry.pack(pady=5)
    entries[col] = entry

def save_new_row():
    new_data = {}
    for col in columns:
        val = entries[col].get().strip()
        new_data[col] = val

    # Append new row to DataFrame
    global df
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

    # Save to CSV
    df.to_csv(CSV_FILE, index=False)

    # Clear entries
    for entry in entries.values():
        entry.delete(0, 'end')

    # Go back to main page or database view
    show_frame(main_frame)

    print("New asset added!")

add_button = ctk.CTkButton(add_row_form_frame, text="Add Asset", font=('Arial', 20, 'bold'),
                           command=save_new_row, width=150, height=60)
add_button.pack(pady=20)

add_row_form_back_button = ctk.CTkButton(add_row_form_frame, text="⬅ Back", font=("Arial", 16),
                                         command=lambda: show_frame(add_frame))
add_row_form_back_button.place(x=1)

add_column_button = ctk.CTkButton(add_frame, text="Add Column", font=('Arial', 20, 'bold'), width=150, height=60, command=lambda: show_frame(manage_columns_frame))
add_column_button.pack(pady=30)

# Title
manage_col_title = ctk.CTkLabel(manage_columns_frame, text="Manage Columns", font=('Arial', 24, 'bold'))
manage_col_title.pack(pady=20)

# Add Column Section
add_col_label = ctk.CTkLabel(manage_columns_frame, text="Add New Column", font=('Arial', 18, 'bold'))
add_col_label.pack(pady=(10,5))

add_col_name_entry = ctk.CTkEntry(manage_columns_frame, placeholder_text="Column Name", width=200)
add_col_name_entry.pack(pady=5)

add_col_default_entry = ctk.CTkEntry(manage_columns_frame, placeholder_text="Default Value (optional)", width=200)
add_col_default_entry.pack(pady=5)

def add_column():
    global df
    new_col = add_col_name_entry.get().strip()
    default_val = add_col_default_entry.get().strip()

    if not new_col:
        print("Column name cannot be empty")
        return

    if new_col in df.columns:
        print("Column already exists!")
        return

    # Add new column with default value or empty string if none provided
    df[new_col] = default_val if default_val else ""

    # Save to CSV
    df.to_csv(CSV_FILE, index=False)

    # Clear inputs
    add_col_name_entry.delete(0, 'end')
    add_col_default_entry.delete(0, 'end')

    load_treeview_data()
    print(f"Column '{new_col}' added!")

add_col_btn = ctk.CTkButton(manage_columns_frame, text="Add Column", command=add_column, width=150, height=50)
add_col_btn.pack(pady=10)

# Delete Column Section
delete_col_label = ctk.CTkLabel(manage_columns_frame, text="Delete Column", font=('Arial', 18, 'bold'))
delete_col_label.pack(pady=(30,5))

# Dropdown for existing columns (excluding "ID" if you want to protect it)
import tkinter as tk
delete_col_var = tk.StringVar(value="Select Column")



def refresh_delete_col_options():
    cols = list(df.columns)
    # Optionally exclude important columns like ID here if needed
    delete_col_dropdown.configure(values=cols)
    delete_col_var.set("Select Column")

delete_col_dropdown = ctk.CTkComboBox(manage_columns_frame, values=list(df.columns), variable=delete_col_var, width=200)
delete_col_dropdown.pack(pady=5)

def delete_column():
    global df
    col_to_delete = delete_col_var.get()

    if col_to_delete not in df.columns:
        print("Select a valid column")
        return

    # Optional: Protect some columns from deletion like ID
    if col_to_delete == "ID":
        print("Cannot delete ID column")
        return

    # Drop column
    df = df.drop(columns=[col_to_delete])

    # Save to CSV
    df.to_csv(CSV_FILE, index=False)

    load_treeview_data()
    refresh_delete_col_options()
    print(f"Column '{col_to_delete}' deleted!")

delete_col_btn = ctk.CTkButton(manage_columns_frame, text="Delete Column", command=delete_column, width=150, height=50)
delete_col_btn.pack(pady=10)

# Back button to go back to add_frame or main_frame
manage_col_back_btn = ctk.CTkButton(manage_columns_frame, text="⬅ Back", font=("Arial", 16),
                                   command=lambda: show_frame(add_frame))
manage_col_back_btn.place(x=1, y=1)

# Refresh delete dropdown options initially
refresh_delete_col_options()


add_back_button = ctk.CTkButton(add_frame, text="⬅ Back", font=("Arial", 16),
                                command=lambda: show_frame(main_frame))
add_back_button.place(x=1)

back_button.place(x=1)

title = ctk.CTkLabel(view_frame, text="Asset Database", font=('Arial', 24, 'bold'))
title.pack(pady=30)

show_frame(main_frame)

tree_frame = ctk.CTkFrame(view_frame)

# --- Search Section ---
search_frame = ctk.CTkFrame(view_frame)
search_frame.pack(pady=10)

search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search...")
search_entry.pack(side="left", padx=10)

def perform_search():
    global df
    search_term = search_entry.get().strip()
    if search_term == "":
        filtered_df = df
    else:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

    update_treeview(filtered_df)

search_button = ctk.CTkButton(search_frame, text="Search", command=perform_search)
search_button.pack(side="left")

clear_button = ctk.CTkButton(search_frame, text="Clear", command=lambda: [search_entry.delete(0, 'end'), load_treeview_data()])
clear_button.pack(side="left", padx=10)


tree_frame.pack(pady=10, padx=10, fill="both", expand=True)


tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")

style = ttk.Style()
style.theme_use("clam")  # Use a style that allows background edits

style.configure("Treeview",
    background="#1e1e1e",         # background of rows
    foreground="white",           # text color
    rowheight=28,
    fieldbackground="#1e1e1e",    # background of the field area
    font=('Arial', 12)
)

style.configure("Treeview.Heading",
    background="#2b2b2b",         # heading background
    foreground="white",           # heading text
    font=('Arial', 13, 'bold')
)

style.map("Treeview", background=[('selected', '#3a3a3a')])  # selected row color


tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
tree.pack(expand=True, fill="both")
tree_scroll.config(command=tree.yview)

def generate_qr_code(row_data):
    # Format the row data into a string for the QR
    qr_content = "\n".join([f"{key}: {row_data.get(key, '')}" for key in row_data])

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(qr_content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to Tkinter-compatible image
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return ImageTk.PhotoImage(Image.open(buffer))

def open_edit_window(event):
    selected = tree.focus()
    if not selected:
        return

    current_values = {col: tree.set(selected, col) for col in tree["columns"]}

    edit_win = ctk.CTkToplevel(window)
    edit_win.title("Edit Asset")
    edit_win.geometry("500x600")  # Wider window for side by side

    # Container frame for side-by-side layout
    container = ctk.CTkFrame(edit_win)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    # Left frame: QR Code
    qr_frame = ctk.CTkFrame(container)
    qr_frame.pack(side="left", fill="y", padx=(0, 10))

    qr_image_pil = None  # To hold the PIL image so we can save it

    def generate_qr_code_image():
        qr_content = ", ".join([f"{key}: {current_values.get(key, '')}" for key in current_values])
        qr = qrcode.QRCode(version=1, box_size=5, border=2)
        qr.add_data(qr_content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img

    qr_image_pil = generate_qr_code_image()
    qr_image_tk = ImageTk.PhotoImage(qr_image_pil)

    qr_label = ctk.CTkLabel(qr_frame, image=qr_image_tk, text="")
    qr_label.image = qr_image_tk  # keep reference
    qr_label.pack(padx=10, pady=180)

    # Right frame: Form
    form_frame = ctk.CTkFrame(container)
    form_frame.pack(side="left", fill="both", expand=True)

    entries_edit = {}

    for col in tree["columns"]:
        label = ctk.CTkLabel(form_frame, text=col, anchor="w")
        label.pack(pady=3, fill='x', padx=10)

        entry = ctk.CTkEntry(form_frame)
        entry.pack(pady=3, padx=10, fill='x')
        entry.insert(0, current_values[col])
        entries_edit[col] = entry

    save_btn = ctk.CTkButton(form_frame, text="Save", width=100, height=40)
    save_btn.pack(pady=20)

    def save_edits():
        global df
        updated_data = {col: entries_edit[col].get().strip() for col in tree["columns"]}
        df.loc[int(selected), :] = pd.Series(updated_data)
        df.to_csv(CSV_FILE, index=False)
        load_treeview_data()
        edit_win.destroy()

    save_btn.configure(command=save_edits)

    # --- New code for right-click download ---

    def save_qr_code(event):
        # Open save file dialog
        file_path = fd.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save QR Code"
        )
        if file_path:
            qr_image_pil.save(file_path)
            print(f"QR code saved to {file_path}")

    qr_label.bind("<Button-1>", save_qr_code)



# Bind single click on row (Treeview selection)
tree.bind("<<TreeviewSelect>>", open_edit_window)

# Define the columns you want to show
tree["columns"] = ("ID", "Model", "Device", "Owner", "Date of Purchase", "Location")

for col in tree["columns"]:
    tree.column(col, anchor="center", width=120)
    tree.heading(col, text=col, anchor="center")

tree.column("#0", width=0, stretch=False)  # Removes the first empty column
tree.column("ID", anchor="center", width=100)
tree.column("Device", anchor="center", width=100)
tree.column("Owner", anchor="center", width=120)

tree.heading("ID", text="ID", anchor="center")
tree.heading("Device", text="Device", anchor="center")
tree.heading("Owner", text="Owner", anchor="center")

window.mainloop()
