import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk  
import mysql.connector                 
from mysql.connector import Error
import subprocess 
import json
import os
import sys

# Connect to MySQL Database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="ROHA",
            password="suggestpassword12",
            database="ecofind_shpping"
        )
        if connection.is_connected():
            print("Connected to MySQL database!")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Fetch all products from ecofnd_products table
def fetch_all_products(connection):
    try:
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True for result as dict
        query = "SELECT * FROM ecofnd_products"
        cursor.execute(query)
        products = cursor.fetchall()
        return products
    except Error as e:
        print(f"Error fetching products: {e}")
        return []

# Function to check and handle login status
def check_login_status():
    try:
        with open('loggedinfo.json', 'r') as file:
            user_info = json.load(file)
        
        # If the JSON is empty or doesn't contain user information
        if not user_info:
            launch_login_page()
            sys.exit()
    except (FileNotFoundError, json.JSONDecodeError):
        launch_login_page()
        sys.exit()

# Function to launch login page
def launch_login_page():
    try:
        subprocess.run(["python", r"D:\Phython_Cedric\Final_Proj\logIN_final.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to launch Login Page. Error: {e}")
    except FileNotFoundError:
        messagebox.showerror("Error", "logIN_final.py not found. Please check the file path.")

# Function to clear JSON file on exit
def on_closing():
    try:
        # Clear the JSON file
        with open('loggedinfo.json', 'w') as file:
            json.dump({}, file)
        
        # Close the database connection if it exists
        if 'db_connection' in globals() and db_connection:
            db_connection.close()
        
        # Destroy the root window
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Error during closing: {e}")

# Insert a new product into ecofnd_products table
def insert_product(connection, product):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO ecofnd_products (name, brand, category, eco_certifications, carbon_footprint, 
                                      recyclable_content, biodegradable, location, sustainability_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            product["name"], product["brand"], product["category"], 
            product["eco_certifications"], product["carbon_footprint"], 
            product["recyclable_content"], product["biodegradable"], 
            product["location"], product["sustainability_score"]
        ))
        connection.commit()
        print(f"Product {product['ProductName']} added successfully.")
    except Error as e:
        print(f"Error inserting product: {e}")


if __name__ == "__main__":
    # Check login status before proceeding
    check_login_status()

    # Connect to the database
    db_connection = connect_to_database()

    if db_connection:
        # Fetch and print all products
        print("Fetching all products...")
        products = fetch_all_products(db_connection)
        for product in products:
            print(product)


# Function to display product details
def show_product_details(product):
    details = f"""
    Name: {product['ProductName']}
    Brand: {product['brand']}
    Category: {product['category']}
    Eco-Certifications: {product['eco_certifications']}
    Carbon Footprint: {product['carbon_footprint']}
    Recyclable Content: {product['recyclable_content']}
    Biodegradable: {product['biodegradable']}
    Location: {product['location']}
    Sustainability Score: {product['sustainability_score']}
    """
    messagebox.showinfo("Product Details", details)


def insert_purchased_product(connection, product):
    try:
        cursor = connection.cursor()
        
        # Fetch the most recent OrderID
        cursor.execute("SELECT MAX(OrderID) FROM orderedproducts")
        last_order_id = cursor.fetchone()[0]
        if last_order_id is None:
            last_order_id = 0
        new_order_id = last_order_id + 1
        
        # Read the logged-in user ID from the JSON file
        with open('loggedinfo.json', 'r') as file:
            user_info = json.load(file)
        user_id_key = next((key for key in user_info.keys() if 'id' in key.lower()), None)
        if not user_id_key:
            raise ValueError("Could not find User ID in logged information")
        user_id = user_info[user_id_key]
        
        insert_query = """
        INSERT INTO orderedproducts (OrderID, User_id, ProductID)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (new_order_id, user_id, product['ProductID']))
        connection.commit()
        print(f"Purchased product {product['ProductName']} added successfully.")
        
        if product not in cart:
            cart.append(product)
            messagebox.showinfo("Added to Comparison", f"{product['ProductName']} added for comparison.")
        else:
            messagebox.showwarning("Already Added", "Product already in comparison list.")
    except Error as e:
        print(f"Error inserting purchased product: {e}")


cart = []
comparison_cart = []
# Function to add product to shopping cart
def add_to_cart(product):
    cart.append(product)
    messagebox.showinfo("Added to Cart", f"{product['ProductName']} has been added to your cart.")

def add_to_comparison(product):
        
    if product not in comparison_cart:
            comparison_cart.append(product)
            messagebox.showinfo("Comparison", f"{product['ProductName']} has been added to the comparison cart.")
    else:
            messagebox.showwarning("Comparison", f"{product['ProductName']} is already in the comparison cart.")


# Function to display comparison
def show_comparison():
    if len(comparison_cart) < 2:
        messagebox.showwarning("Comparison", "Please add at least 2 products to compare.")
        return

    global comparison_window
    comparison_window = tk.Toplevel(root)
    comparison_window.title("Product Comparison")

    for idx, product in enumerate(comparison_cart):
        frame = tk.Frame(comparison_window, relief="solid", bd=1, padx=5, pady=5)
        frame.grid(row=0, column=idx, padx=10, pady=10)

        tk.Label(frame, text=f"Name: {product['ProductName']}").pack(anchor="w")
        tk.Label(frame, text=f"Brand: {product['brand']}").pack(anchor="w")
        tk.Label(frame, text=f"Carbon Footprint: {product['carbon_footprint']}").pack(anchor="w")
        tk.Label(frame, text=f"Recyclable Content: {product['recyclable_content']}").pack(anchor="w")
        tk.Label(frame, text=f"Biodegradable: {product['biodegradable']}").pack(anchor="w")

        # Remove button for the product
        ctk.CTkButton(frame, text="Remove", command=lambda p=product: (comparison_cart.remove(p), comparison_window.destroy(), show_comparison()), fg_color="red", text_color="white", corner_radius=10).pack(pady=5)

    # Close button
    ctk.CTkButton(comparison_window, text="Close", command=comparison_window.destroy, fg_color="lightgray", text_color="black", corner_radius=10).pack(pady=10)



# Function to add placeholder text to search entry
def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.bind("<FocusIn>", lambda event: clear_placeholder(entry, placeholder_text))
    entry.bind("<FocusOut>", lambda event: reset_placeholder(entry, placeholder_text))

def clear_placeholder(entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, "end")
        entry.config(fg="black")

def reset_placeholder(entry, placeholder_text):
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(fg="gray")



# Function to show purchase window
def show_purchase():
    try:
        # Read logged-in user info from JSON file
        with open('loggedinfo.json', 'r') as file:
            user_info = json.load(file)

        # Find the correct key for User ID
        user_id_key = next((key for key in user_info.keys() if "user_id" in key.lower()), None)
        if not user_id_key:
            messagebox.showerror("Error", "Could not find User ID in logged information")
            return
        user_id = user_info[user_id_key]

        # Check if cart is not empty
        if not cart:
            messagebox.showinfo("Cart", "Your cart is empty.")
            return

        # Extract ProductIDs from the cart
        product_ids = [product['ProductID'] for product in cart]

        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="ROHA",
            password="suggestpassword12",
            database="ecofind_shpping"
        )
        if not connection.is_connected():
            messagebox.showerror("Error", "Failed to connect to the database.")
            return

        cursor = connection.cursor()

        # Fetch products in the user's cart
        cart_query = "SELECT * FROM ecofnd_products WHERE ProductID IN (%s)"
        formatted_query = cart_query % ', '.join(['%s'] * len(product_ids))
        cursor.execute(formatted_query, tuple(product_ids))
        cart_products = cursor.fetchall()

        # Insert purchased products into the orderedproducts table
        insert_query = "INSERT INTO orderedproducts (OrderID, User_id, ProductID) VALUES (%s, %s, %s)"
        for product in cart_products:
            try:
                # Assuming ProductID is the first column in the query result
                cursor.execute(insert_query, (None, user_id, product[0]))
            except Error as e:
                print(f"Error inserting product {product[0]}: {e}")
                continue


        # Commit the transaction
        connection.commit()

        messagebox.showinfo("Purchase Successful", "Your products have been added to your purchase history.")

        # Clear the cart
        cart.clear()

    except FileNotFoundError:
        messagebox.showerror("Error", "No user currently logged in.")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
    except Exception as e:
        messagebox.showerror("Unexpected Error", str(e))
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
                
def launch_purchased_products():

    try:
        
        subprocess.run(["python", r"D:\Phython_Cedric\Final_Proj\Purchased_product.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to launch Purchased Products. Error: {e}")
    except FileNotFoundError:
        messagebox.showerror("Error", "Purchased_product.py not found. Please check the file path.")


class PurchaseButton:
    def __init__(self, master):
        self.purchase_button = ctk.CTkButton(
            master, 
            text="View Purchases", 
            command=self.open_purchased_products
        )
        self.purchase_button.pack()  # or grid/place as needed

    def open_purchased_products(self):
        try:
            # Replace with the actual path to your Purchased_product.py
            subprocess.run(["python", r"D:\Phython_Cedric\Final_Proj\Purchased_product.py"], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to launch Purchased Products. Error: {e}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Purchased_product.py not found. Please check the file path.")

# Function to show cart contents
# Function to show cart contents
def show_cart():
    if not cart:
        messagebox.showinfo("Cart", "Your cart is empty.")
        return

    def refresh_cart():
        cart_window.destroy()
        show_cart()

    def proceed_to_purchase():
        cart_window.destroy()  # Close the cart window
        show_purchase()  # Proceed to purchase

    cart_window = tk.Toplevel(root)
    cart_window.title("Shopping Cart")

    cart_window.configure(bg="white")

    tk.Label(cart_window, text="Products in Cart", font=("Helvetica", 14, "bold"),bg="white",fg="green").pack(pady=10)

    for product in cart:
        frame = tk.Frame(cart_window, relief="solid", bd=1, padx=5, pady=5)
        frame.pack(pady=5, fill="x")

        tk.Label(frame, text=f"Name: {product['ProductName']}").pack(anchor="w")
        tk.Label(frame, text=f"Brand: {product['brand']}").pack(anchor="w")
        tk.Label(frame, text=f"Category: {product['category']}").pack(anchor="w")
        tk.Label(frame, text=f"Sustainability Score: {product['sustainability_score']}").pack(anchor="w")

    
        ctk.CTkButton(frame, text="Remove", command=lambda p=product: (cart.remove(p), refresh_cart()),fg_color="red", text_color="white", corner_radius=10).pack(side="right", padx=5)


    # Button to open the purchase window, now closing cart window before purchasing
    ctk.CTkButton(cart_window, text="Proceed to Purchase", command=proceed_to_purchase, fg_color="limegreen", text_color="black", corner_radius=10).pack(pady=10)

# Main GUI setup
root = tk.Tk()
root.title("Eco-Friendly Product Database")
root.configure(bg="white")


headline_label = tk.Label(root, text="Welcome to the Eco-Friendly Product Database", 
                          bg="green", fg="white", font=("Helvetica", 18, "bold"))
headline_label.pack(fill="x")


top_frame = tk.Frame(root)
top_frame.pack(side="top", fill="x", pady=10)

# Function to return to the main product display
def show_all_products():
    display_products(products)  

# Logo Label as Hyperlink
logo_hyperlink = tk.Label(
    top_frame,
    text="EcoFind",
    font=("Helvetica", 22, "bold underline"), 
    fg="Green", 
    cursor="hand2"  
)
logo_hyperlink.grid(row=0, column=0, padx=10, sticky="w")


logo_hyperlink.bind("<Button-1>", lambda e: show_all_products())


search_frame = tk.Frame(top_frame)
search_frame.grid(row=0, column=1, padx=10)

def clear_placeholder_on_focus(event):
    if search_entry.get() == "Search Products":
        search_entry.delete(0, "end")  
        search_entry.configure(text_color="black")  

def reset_placeholder_on_focus_out(event):
    if search_entry.get() == "":  
        search_entry.insert(0, "Search Products")  
        search_entry.configure(text_color="gray") 

search_entry = ctk.CTkEntry(
    search_frame, 
    width=200, 
    corner_radius=10, 
    placeholder_text="",
    fg_color="white", 
    text_color="gray"  
)
search_entry.insert(0, "Search Products")
search_entry.grid(row=0, column=0, padx=(0, 5))

# Bind events for placeholder behavior
search_entry.bind("<FocusIn>", clear_placeholder_on_focus)
search_entry.bind("<FocusOut>", reset_placeholder_on_focus_out)

# Search entry with placeholder
search_entry = ctk.CTkEntry(search_frame, width=200, corner_radius=10, placeholder_text="Search Products", fg_color="white", text_color="black")
search_entry.insert(0, "Search Products")
search_entry.grid(row=0, column=0, padx=(0, 5))  

# Search button directly to the right of search bar
ctk.CTkButton(search_frame, text="Search", 
              command=lambda: search_products(search_entry.get()), 
              fg_color="lightgreen", text_color="black", 
              corner_radius=10,width =70,height = 20).grid(row=0, column=1)

# Filter options on the right side of the top frame
filter_frame = tk.Frame(top_frame)
filter_frame.grid(row=0, column=2, padx=10, sticky="e")

# Add filter labels and dropdowns
tk.Label(filter_frame, text="Filter by Category").pack(side="left")
category_combo = ttk.Combobox(filter_frame, values=["All", "Cleaning", "Clothing", "Electronics"],width = 18)
category_combo.set("All")
category_combo.pack(side="left", padx=5)

tk.Label(filter_frame, text="Filter by Carbon Footprint").pack(side="left")
footprint_combo = ttk.Combobox(filter_frame, values=["All", "Low", "Medium", "High"],width = 18)
footprint_combo.set("All")
footprint_combo.pack(side="left", padx=5)

def apply_filters():
    # Get selected filters
    selected_category = category_combo.get()
    selected_footprint = footprint_combo.get()

    # Filter products based on selected category and carbon footprint
    filtered_products = products

    if selected_category != "All":
        filtered_products = [p for p in filtered_products if p['category'] == selected_category]

    if selected_footprint != "All":
        filtered_products = [
            p for p in filtered_products
            if (selected_footprint == "Low" and int(p['carbon_footprint'].split("g")[0]) <= 100) or
               (selected_footprint == "Medium" and 100 < int(p['carbon_footprint'].split("g")[0]) <= 200) or
               (selected_footprint == "High" and int(p['carbon_footprint'].split("g")[0]) > 200)
        ]

    # Update the product list with filtered products
    display_products(filtered_products)

# Apply Filters Button
ctk.CTkButton(filter_frame, text="Apply Filters", command=apply_filters, 
              fg_color="lightgreen",text_color = "black", corner_radius=10,height = 20,width=70).pack(side="left", padx=5)

# Add View Cart and Compare Products Buttons beside Apply Filters
ctk.CTkButton(filter_frame, text="View Cart", command=show_cart, 
              fg_color="skyblue",text_color = "black", corner_radius=10,height = 20,width= 70).pack(side="left", padx=5)
ctk.CTkButton(filter_frame, text="Compare", command=show_comparison, 
              fg_color="lightgreen",text_color = "black", corner_radius=10,height = 20,width=100).pack(side="left", padx=5)


def display_products(product_list):
    # Clear the product list frame before updating it
    for widget in product_list_frame.winfo_children():
        widget.destroy()

    # Ensure proper grid layout configuration
    row = 0
    col = 0
    for product in product_list:
        # Create a new frame for each product
        frame = tk.Frame(product_list_frame, relief="solid", bd=1, padx=5, pady=5,bg="white")
        frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")  # Use grid for proper layout
        
        # Add product details to the frame
        tk.Label(frame, text=f"{product['ProductName']} ({product['brand']})",bg="white").pack(anchor="w")
        tk.Label(frame, text=f"Category: {product['category']}, Score: {product['sustainability_score']}",bg="white").pack(anchor="w")

        # Add buttons to the frame
        tk.Button(frame, text="View Details", command=lambda p=product: show_product_details(p),bg="limegreen").pack(side="left", padx=5)
        tk.Button(frame, text="Add to Comparison", command=lambda p=product: add_to_comparison(p),bg="skyblue").pack(side="left", padx=5)
        tk.Button(frame, text="Add to Cart", command=lambda p=product: add_to_cart(p),bg="limegreen").pack(side="left", padx=5)


        col += 1
        if col > 3:  
            col = 0
            row += 1
  

def search_products(query):
    # Clear any existing products in the display frame
    for widget in product_list_frame.winfo_children():
        widget.destroy()

    # Filter products based on the query
    query = query.lower()
    filtered_products = [
        product for product in products
        if query in product['ProductName'].lower() or query in product['brand'].lower() or query in product['category'].lower()
    ]

# Search-related functions

def search_products(query):
    # Clear any existing products in the display frame
    for widget in product_list_frame.winfo_children():
        widget.destroy()

    # Convert the query to lowercase for case-insensitive search
    query = query.lower()

    # Filter products based on the query
    filtered_products = [
        product for product in products
        if query in product['ProductName'].lower() or query in product['brand'].lower() or query in product['category'].lower()
    ]

    # If no products match the search, display a message
    if not filtered_products:
        tk.Label(product_list_frame, text="No products match your search.", font=("Helvetica", 14), fg="red").pack(pady=10)
        return

    # Display the filtered products
    display_products(filtered_products)

    
# Product List

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root,orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side ="right",fill="y")
canvas.pack(pady = 9, fill="both",expand=True)
product_list_frame = tk.Frame(root)
product_list_frame.pack(pady=5, fill="both", expand=True)

canvas.create_window((0, 0), window=product_list_frame, anchor="nw")

def on_mousewheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

# Update canvas scroll region whenever its content changes
def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

product_list_frame.bind("<Configure>", update_scroll_region)

canvas.pack(pady=10, fill="both", expand=True)

columns = 4

for idx, product in enumerate(products):
    row = idx // columns + 1 
    column = idx % columns     

    # Create a frame for each product in the grid layout
    frame = tk.Frame(product_list_frame, relief="solid", bd=1, padx=5, pady=5,bg="white")
    frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

    # Add product details and buttons
    tk.Label(frame, text=f"{product['ProductName']} ({product['brand']})",bg="white").pack(anchor="w")
    tk.Label(frame, text=f"Category: {product['category']}, Score: {product['sustainability_score']}",bg="white").pack(anchor="w")

    # Buttons for actions
    tk.Button(frame, text="View Details", command=lambda p=product: show_product_details(p),bg="limegreen").pack(side="left", padx=5)
    tk.Button(frame, text="Add to Comparison", command=lambda p=product: add_to_comparison(p),bg="skyblue").pack(side="left", padx=5)
    tk.Button(frame, text="Add to Cart", command=lambda p=product: add_to_cart(p),bg="limegreen").pack(side="left", padx=5)


# Make the columns expand proportionally to fill the window
for col in range(columns):
    product_list_frame.grid_columnconfigure(col, weight=1)


root.protocol("WM_DELETE_WINDOW", on_closing)
# Run the GUI
root.mainloop()
# Close the database connection
if 'db_connection' in locals() and db_connection:
    db_connection.close()