from tkinter import *
from tkinter import ttk, messagebox 
from PIL import Image, ImageTk
import pymysql


class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")  # Change window background color

        # === Background Image ===
        self.bg = ImageTk.PhotoImage(file=r"c:\online voting application\images\andy-holmes-LUpDjlJv4_c-unsplash (1).jpg")
        bg = Label(self.root, image=self.bg).place(x=250, y=0, relwidth=1, relheight=1)

        # === Left Image ===
        self.left = ImageTk.PhotoImage(file=r"c:\online voting application\images\istockphoto-1083674480-612x612.jpg")
        left = Label(self.root, image=self.left).place(x=80, y=100, width=400, height=500)

        # === Register Frame ===
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=480, y=100, width=700, height=500)

        title = Label(frame1, text="REGISTER HERE", font=("times new roman", 20, "bold"), bg="white", fg="green")
        title.place(x=50, y=30)

        # === First Row ===
        Label(frame1, text="FIRST NAME", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=100)
        self.txt_fname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_fname.place(x=50, y=130, width=250)

        Label(frame1, text="LAST NAME", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=100)
        self.txt_lname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_lname.place(x=370, y=130, width=250)

        # === Second Row ===
        Label(frame1, text="CONTACT NUMBER", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=170)
        self.txt_f_contact = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_f_contact.place(x=50, y=200, width=250)

        Label(frame1, text="EMAIL ID", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=170)
        self.txt_email = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=370, y=200, width=250)

        # === Third Row ===
        Label(frame1, text="SECURITY QUESTION", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=240)
        self.cmb_quest = ttk.Combobox(frame1, font=("times new roman", 13), state="readonly", justify=CENTER)
        self.cmb_quest['values'] = ("Select", "Your date of birth", "Your pet's name", "Your address")
        self.cmb_quest.place(x=50, y=270, width=250)
        self.cmb_quest.current(0)  # Default selection

        Label(frame1, text="ANSWER", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=240)
        self.answer = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.answer.place(x=370, y=270, width=250)

        # === Fourth Row (Password) ===
        Label(frame1, text="PASSWORD", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=310)
        self.txt_password = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_password.place(x=50, y=340, width=250)

        Label(frame1, text="CONFIRM PASSWORD", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=310)
        self.txt_cpassword = Entry(frame1, font=("times new roman", 15), bg="lightgray")  # Fix variable name
        self.txt_cpassword.place(x=370, y=340, width=250)

        # === Register Button ===
        self.btn_img = ImageTk.PhotoImage(file=r"c:\online voting application\images\images.jpg")
        btn = Button(frame1, image=self.btn_img, bd=0, cursor="hand2", command=self.register_data)  
        btn.place(x=50, y=400)

#singin button
        btn = Button(self.root, text="sign in",command=self.login_window, font=("times new roman", 20, "bold"),bd=0, cursor="hand2" ) 
        btn.place(x=200, y=460,width=180)
        
     #<----regesiter login after sumbit--->
    def login_window(self):
        self.root.destroy()
        import login1   
        
    # === register_data Method ===
    def clear(self):  # HELP TO DELETE DATA AFTER FORM IS SUBMITTED
        self.txt_fname.delete(0, END)
        self.txt_lname.delete(0, END)
        self.txt_f_contact.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_password.delete(0, END)
        self.txt_cpassword.delete(0, END)
        self.cmb_quest.delete(0, END)
        self.answer.delete(0, END)
   
    def register_data(self):
        error_messages = []  # List to store error messages
# if name is empty and submit it show and apend add 
        if self.txt_fname.get() == "":
            error_messages.append("First name is required.")
        if self.txt_lname.get() == "":
            error_messages.append("Last name is required.")
        if self.txt_f_contact.get() == "":
            error_messages.append("Contact number is required.")
        if self.txt_email.get() == "":
            error_messages.append("Email is required.")
        if self.cmb_quest.get() == "Select":
            error_messages.append("Security question is required.")
        if self.answer.get() == "":
            error_messages.append("Answer is required.")
        if self.txt_password.get() == "":
            error_messages.append("Password is required.")
        if self.txt_cpassword.get() == "":
            error_messages.append("Confirm password is required.")

        if len(error_messages) > 0:
            messagebox.showerror("Error", "\n".join(error_messages), parent=self.root)
            return
        #the above code show the meesage if the filled is not filled

        # === Fix: Strip extra spaces from password and confirm password ===
        password = self.txt_password.get().strip()  # Remove leading/trailing spaces from password
        confirm_password = self.txt_cpassword.get().strip()  # Remove leading/trailing spaces from confirm password

        if password != confirm_password:  # Now comparing stripped values
            messagebox.showerror("Error", "Password and confirm password should be the same", parent=self.root)
        else:
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="employee2")
                cur = con.cursor()
                cur.execute("select * from employee where email=%s", self.txt_email.get())
                row = cur.fetchone()
                if row is not None:  # Check if the email already exists
                    messagebox.showerror("Error", "Username already exists", parent=self.root)
                else:
                    cur.execute("insert into employee (f_name,l_name,contact,email,question,answer,password)values(%s,%s,%s,%s,%s,%s,%s)",
                                 (self.txt_fname.get(),
                                  self.txt_lname.get(),
                                  self.txt_f_contact.get(),
                                  self.txt_email.get(),
                                  self.cmb_quest.get(),
                                  self.answer.get(),
                                  self.txt_password.get()
                                 ))
                    con.commit()  # Enter data in database
                    con.close()
                    messagebox.showinfo("Successful", "Your account has been created", parent=self.root)
                    self.clear()

            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

# === Run Application ===
root = Tk()
obj = Register(root)
root.mainloop()
