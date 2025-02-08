import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  
import pymysql

# Create main window
master = tk.Tk()
master.title("Login Form")
master.geometry(f"{master.winfo_screenwidth()}x{master.winfo_screenheight()}")
master.config(bg="#e3e3e3")
master.state("zoomed")

# Load and display image
image_path = "c:\online voting application\images\Picture1.png"
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()

image = Image.open(image_path)
aspect_ratio = image.width / image.height
new_width = screen_width // 2
new_height = int(new_width / aspect_ratio)
image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(image)

# Create main container frame
main_frame = tk.Frame(master, bg="#e3e3e3")
main_frame.place(relx=0.5, rely=0.55, anchor="center")

# Image Label
img_label = tk.Label(main_frame, image=img, bg="#e3e3e3", bd=0, relief="flat", highlightthickness=0)
img_label.pack(side="left", padx=10, pady=10)

# Login Frame
login_frame = tk.Frame(main_frame, width=new_width, height=new_height, bg="#ffffff")
login_frame.pack(side="right", padx=0)
login_frame.grid_propagate(False)

# Center content inside login frame
inner_frame = tk.Frame(login_frame, bg="#ffffff")
inner_frame.place(relx=0.5, rely=0.5, anchor="center")

# Heading Label
heading = tk.Label(inner_frame, text="Welcome Back!", fg="#0056b3", bg="#ffffff", font=("Bookman Old Style", 24, "bold"))
heading.pack(pady=20)

# Username Entry
fixed_username_label = tk.Label(inner_frame, text="Gmail ID", fg="#333", bg="#ffffff", font=("Bookman Old Style", 14))
fixed_username_label.pack()
user_name = tk.Entry(inner_frame, width=30, fg="black", border=2, relief="solid", bg="#f8f8f8", font=("Arial", 12))
user_name.pack(pady=5)
tk.Frame(inner_frame, width=250, height=2, bg="#57a1f8").pack()

# Password Entry
def toggle_password():
    if user_password.cget('show') == "*":
        user_password.config(show="")
    else:
        user_password.config(show="*")

password_label = tk.Label(inner_frame, text="Password", fg="#333", bg="#ffffff", font=("Bookman Old Style", 14))
password_label.pack()
user_password = tk.Entry(inner_frame, width=30, fg="black", border=2, relief="solid", bg="#f8f8f8", show="*", font=("Arial", 12))
user_password.pack(pady=10)
tk.Frame(inner_frame, width=250, height=2, bg="#57a1f8").pack()

# Show Password Checkbox
show_password_var = tk.IntVar()
show_password_check = tk.Checkbutton(inner_frame, text="Show Password", variable=show_password_var, bg="#ffffff", command=toggle_password, font=("Arial", 10))
show_password_check.pack(pady=5)

# Function to Verify Login
def login():
    gmail = user_name.get().strip()
    password = user_password.get().strip()

    if not gmail or not password:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        # Connect to MySQL database
        conn = pymysql.connect(host="localhost", user="root", password="", database="employee2")
        cursor = conn.cursor()

        # Fetch email & password from the database
        query = "SELECT email, password FROM employee WHERE email = %s AND password = %s"
        cursor.execute(query, (gmail, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", "Login Successful!")
            master.destroy()  # Close the login window
            # Open your main application window here
        else:
            messagebox.showerror("Error", "Invalid Email or Password!")

    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{str(e)}")

    finally:
        if conn:
            conn.close()  # Ensure connection is closed

# Register Window Function (just open your REGISTER page)
def register_window():
    master.destroy()  # Close the login window
    import REGISTER  # Make sure REGISTER.py exists and is coded properly
    #<----if the password match the critea login to next page----->
def login_window():
    master.destroy()
    import content1



# Login Button
login_button = tk.Button(inner_frame, width=25, pady=10, text="Log in",command=login_window, bg="#0056b3", fg="white", border=0, font=("Arial", 14, "bold"), relief="raised", cursor="hand2")
login_button.pack(pady=20)

# No Account Label
no_account_label = tk.Label(inner_frame, text="Don't have an account?", fg="#333", bg="#ffffff", font=("Bookman Old Style", 10))
no_account_label.pack()

# Sign Up Button
sign_up = tk.Button(inner_frame, text="Sign up", border=0, bg="#ffffff", cursor="hand2", command=register_window, fg="#0056b3", font=("Arial", 12, "bold"))
sign_up.pack()

# Run the application
master.mainloop()
