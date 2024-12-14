import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk  
import mysql.connector  
import re 
import subprocess  
import json
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'ROHA',
    'password': 'suggestpassword12',
    'database': 'ecofind_shpping'
}

# Path for the logged user info file
LOGGED_INFO_PATH = os.path.join(os.path.dirname(__file__), 'loggedinfo.json')

# Function to save logged-in user information
def save_logged_user_info(user_id, username):
    try:
        # Create a dictionary with user information
        user_info = {
            "user_id": user_id,
            "username": username
        }
        
        # Write user info to JSON file
        with open(LOGGED_INFO_PATH, 'w') as file:
            json.dump(user_info, file, indent=4)
        
        return True
    except Exception as e:
        messagebox.showerror("File Error", f"Could not save user information: {e}")
        return False
    
# Function to validate phone number
def is_valid_phone_number(phone):
    # Remove any spaces or dashes
    phone = re.sub(r'[\s-]', '', phone)
    # Check if the phone number is 10 digits long and starts with a valid prefix
    return re.match(r'^(9|8|7|6)\d{9}$', phone) is not None

def validate_credentials():
    username = username_entry.get()
    password = password_entry.get()

    try:
        # Establish database connection
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Check credentials against the database
        query = "SELECT user_id, username FROM user WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            # Save user info to JSON file
            if save_logged_user_info(user['user_id'], user['username']):
                messagebox.showinfo("Login", f"Welcome, {username}!")
                
                try:
                    # Close the current login window
                    root.destroy()
                    
                    # Launch main_dash.py
                    subprocess.run(["python", r"D:\Phython_Cedric\Final_Proj\main_dash.py"], check=True)
                
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error", f"Failed to launch main dashboard. Error: {e}")
                except FileNotFoundError:
                    messagebox.showerror("Error", "main_dash.py not found. Please check the file path.")
            else:
                messagebox.showerror("Login Error", "Failed to save user information.")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def back_from_login():
    # Hide login fields
    username_label.pack_forget()
    username_entry.pack_forget()
    password_label.pack_forget()
    password_entry.pack_forget()
    submit_button.pack_forget()
    login_back_button.pack_forget()

    # Restore initial buttons
    login_button.pack(pady=(150, 10))
    reg_button.pack(pady=(0, 10))

# Function to show login fields
def show_login_fields():
    # Hide initial buttons
    login_button.pack_forget()  
    reg_button.pack_forget()
    
    try:
        register_username_entry.pack_forget()
        register_password_entry.pack_forget()
        confirm_password_entry.pack_forget()
        register_submit_button.pack_forget()
        register_back_button.pack_forget()
        register_buttons_frame.pack_forget()
    except:
        pass
    
    # Display Username and Password fields
    username_label.pack(pady=(50, 5))
    username_entry.pack(pady=(0, 20))
    password_label.pack(pady=(10, 5))
    password_entry.pack(pady=(0, 20))
    submit_button.pack(pady=(20, 10))
    login_back_button.pack(pady=(10, 30))

# Function to return to initial screen from registration
def back_from_register():
    # Hide registration fields
    register_username_label.pack_forget()
    register_username_entry.pack_forget()
    register_password_label.pack_forget()
    register_password_entry.pack_forget()
    confirm_password_label.pack_forget()
    confirm_password_entry.pack_forget()
    contact_number_label.pack_forget()
    contact_number_entry.pack_forget()
    address_label.pack_forget()
    address_entry.pack_forget()
    register_buttons_frame.pack_forget()

    # Restore initial buttons
    login_button.pack(pady=(150, 10))
    reg_button.pack(pady=(0, 10))

def open_register_form():
    # Hide initial buttons
    login_button.pack_forget()  
    reg_button.pack_forget()

    try:
        username_label.pack_forget()
        username_entry.pack_forget()
        password_label.pack_forget()
        password_entry.pack_forget()
        submit_button.pack_forget()
        login_back_button.pack_forget()
    except:
        pass

    # Username field
    global register_username_label
    register_username_label = ctk.CTkLabel(right_frame, text="Username", font=("Helvetica", 16), text_color="black")
    register_username_label.pack(pady=(10, 5))
    
    global register_username_entry
    register_username_entry = ctk.CTkEntry(right_frame, width=300, height=40, corner_radius=10)
    register_username_entry.pack(pady=(0, 20))

    # Password field
    global register_password_label
    register_password_label = ctk.CTkLabel(right_frame, text="Password", font=("Helvetica", 16), text_color="black")
    register_password_label.pack(pady=(10, 5))
    
    global register_password_entry
    register_password_entry = ctk.CTkEntry(right_frame, show="*", width=300, height=40, corner_radius=10)
    register_password_entry.pack(pady=(0, 20))

    # Confirm Password field
    global confirm_password_label
    confirm_password_label = ctk.CTkLabel(right_frame, text="Confirm Password", font=("Helvetica", 16), text_color="black")
    confirm_password_label.pack(pady=(10, 5))
    
    global confirm_password_entry
    confirm_password_entry = ctk.CTkEntry(right_frame, show="*", width=300, height=40, corner_radius=10)
    confirm_password_entry.pack(pady=(0, 20))

    # Contact Number field
    global contact_number_label
    contact_number_label = ctk.CTkLabel(right_frame, text="Contact Number", font=("Helvetica", 16), text_color="black")
    contact_number_label.pack(pady=(10, 5))
    
    global contact_number_entry
    contact_number_entry = ctk.CTkEntry(right_frame, width=300, height=40, corner_radius=10)
    contact_number_entry.pack(pady=(0, 20))

    # Address field
    global address_label
    address_label = ctk.CTkLabel(right_frame, text="Address", font=("Helvetica", 16), text_color="black")
    address_label.pack(pady=(10, 5))
    
    global address_entry
    address_entry = ctk.CTkEntry(right_frame, width=300, height=40, corner_radius=10)
    address_entry.pack(pady=(0, 20))

    # Buttons frame
    global register_buttons_frame
    register_buttons_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
    register_buttons_frame.pack(pady=(20, 30))

    # Submit and Back buttons
    global register_submit_button
    register_submit_button = ctk.CTkButton(
        register_buttons_frame, text="REGISTER", font=("Helvetica", 16), text_color="black", 
        fg_color="limegreen", corner_radius=15, command=register_user, width=150, height=50
    )
    register_submit_button.pack(side="left", padx=(0, 10))

    global register_back_button
    register_back_button = ctk.CTkButton(
        register_buttons_frame, text="BACK", font=("Helvetica", 16), text_color="black", 
        fg_color="gray", corner_radius=15, command=back_from_register, width=150, height=50
    )
    register_back_button.pack(side="left")

# Function to register a new user
def register_user():
    username = register_username_entry.get()
    password = register_password_entry.get()
    confirm_password = confirm_password_entry.get()
    contact_number = contact_number_entry.get()
    address = address_entry.get()

    # Validation checks
    if not username or not password or not confirm_password or not contact_number or not address:
        messagebox.showerror("Error", "All fields are required!", parent=root)
        return
    
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!", parent=root)
        return



    try:
        # Establish database connection
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Update query to include contact number and address
        query = "INSERT INTO user (username, password, contact_number, address) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, password, contact_number, address))
        connection.commit()  # Save changes to the database
    
        messagebox.showinfo("Success", "Registration successful!", parent=root)

        # Clear all entries
        register_username_entry.delete(0, tk.END)
        register_password_entry.delete(0, tk.END)
        confirm_password_entry.delete(0, tk.END)
        contact_number_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)

        back_from_register()

    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username already exists. Please choose a different username.", parent=root)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}", parent=root)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
    register_username_label.pack_forget()
    register_username_entry.pack_forget()
    register_password_label.pack_forget()
    register_password_entry.pack_forget()
    confirm_password_label.pack_forget()
    confirm_password_entry.pack_forget()
    register_buttons_frame.pack_forget()
    
    login_button.pack(pady=(150, 10))
    reg_button.pack(pady=(0, 10))

# Initialize the main window
root = ctk.CTk() 
root.geometry("800x800")  
root.title("EcoFind")

# Set green theme for the app
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("green") 

# Configure grid layout for the root window
root.grid_columnconfigure(0, weight=1)  
root.grid_columnconfigure(1, weight=1)  
root.grid_rowconfigure(0, weight=1) 


left_frame = ctk.CTkFrame(root, fg_color="#a8df65", corner_radius=0)
left_frame.grid(row=0, column=0, sticky="nsew")


right_frame = ctk.CTkFrame(root, fg_color="#f0f4c3", corner_radius=0)
right_frame.grid(row=0, column=1, sticky="nsew")

title_label = ctk.CTkLabel(left_frame, text="EcoFind", font=("Helvetica", 36, "bold"), text_color="green")
title_label.pack(expand=True, pady=50)

# (Initial Login button and fields)
# Log In button
login_button = ctk.CTkButton(
    right_frame, text="LOG IN", font=("Helvetica", 16), text_color="black", 
    fg_color="limegreen", corner_radius=15, command=show_login_fields, width=200, height=50
)
login_button.pack(pady=(150, 10))  # Added padding to create space above and between buttons


reg_button = ctk.CTkButton(
    right_frame, text="REGISTER", font=("Helvetica", 16), text_color="black", 
    fg_color="limegreen", corner_radius=15, command=open_register_form, width=200, height=50
)
reg_button.pack(pady=(0, 10))  # No padding above; only space below

# Username and Password labels and entries
username_label = ctk.CTkLabel(right_frame, text="Username", font=("Helvetica", 16), text_color="black")
username_entry = ctk.CTkEntry(right_frame, width=300, height=40, corner_radius=10)

password_label = ctk.CTkLabel(right_frame, text="Password", font=("Helvetica", 16), text_color="black")
password_entry = ctk.CTkEntry(right_frame, show="*", width=300, height=40, corner_radius=10)

# Submit button for validating credentials
submit_button = ctk.CTkButton(
    right_frame, text="SUBMIT", font=("Helvetica", 16), text_color="black", 
    fg_color="limegreen", corner_radius=15, command=validate_credentials, width=200, height=50
)

# Back button for login
login_back_button = ctk.CTkButton(
    right_frame, text="BACK", font=("Helvetica", 16), text_color="black", 
    fg_color="gray", corner_radius=15, command=back_from_login, width=200, height=50
)



root.mainloop()