import tkinter as tk
from tkinter import messagebox
import mysql.connector
import matplotlib.pyplot as plt

# Database Setup
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="employee2"
    )

def setup_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            position VARCHAR(255) NOT NULL,
            votes INT DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voters (
            username VARCHAR(255) PRIMARY KEY,
            voted INT DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Tkinter Window
root = tk.Tk()
root.title("Vote Ed")
root.geometry("400x300")

def main_menu():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Voted Ed", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="User", width=20, height=2, command=user_login).pack(pady=10)
    tk.Button(root, text="Admin", width=20, height=2, command=admin_login).pack(pady=10)

def admin_login():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Admin Login", font=("Arial", 14)).pack(pady=20)
    tk.Label(root, text="Username").pack()
    admin_user = tk.Entry(root)
    admin_user.pack()
    
    tk.Label(root, text="Password").pack()
    admin_pass = tk.Entry(root, show="*")
    admin_pass.pack()
    
    def validate_admin():
        if admin_user.get() == "1" and admin_pass.get() == "1":
            admin_panel()
        else:
            messagebox.showerror("Error", "Invalid Admin Credentials")
    
    tk.Button(root, text="Login", command=validate_admin).pack(pady=10)
    tk.Button(root, text="Back", command=main_menu).pack()

def admin_panel():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Admin Panel", font=("Arial", 14)).pack(pady=20)
    tk.Button(root, text="Add Candidate", width=20, height=2, command=add_candidate).pack(pady=10)
    tk.Button(root, text="View Result", width=20, height=2, command=view_result).pack(pady=10)
    tk.Button(root, text="Clear Votes", width=20, height=2, command=clear_votes).pack(pady=10)
    tk.Button(root, text="Logout", width=20, height=2, command=main_menu).pack(pady=10)

def add_candidate():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Add Candidate", font=("Arial", 14)).pack(pady=20)
    tk.Label(root, text="Candidate Name").pack()
    candidate_name = tk.Entry(root)
    candidate_name.pack()
    
    tk.Label(root, text="Position").pack()
    candidate_position = tk.Entry(root)
    candidate_position.pack()
    
    def save_candidate():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO candidates (name, position) VALUES (%s, %s)", (candidate_name.get(), candidate_position.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Candidate Added Successfully")
        admin_panel()
    
    tk.Button(root, text="Add", command=save_candidate).pack(pady=10)
    tk.Button(root, text="Back", command=admin_panel).pack()

def clear_votes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE candidates SET votes = 0")
    cursor.execute("DELETE FROM voters")
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "All votes have been cleared")

def user_login():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="User Panel", font=("Arial", 14)).pack(pady=20)
    tk.Button(root, text="Candidate List & Vote", width=20, height=2, command=user_vote).pack(pady=10)
    tk.Button(root, text="View Results", width=20, height=2, command=view_result).pack(pady=10)
    tk.Button(root, text="Logout", width=20, height=2, command=main_menu).pack(pady=10)

def view_result():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, votes FROM candidates")
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        messagebox.showinfo("Results", "No candidates available yet.")
        return
    
    names = [r[0] for r in results]
    votes = [r[1] for r in results]
    winner = names[votes.index(max(votes))]
    
    plt.figure(figsize=(6,6))
    plt.pie(votes, labels=names, autopct='%1.1f%%', startangle=140)
    plt.title(f"Election Results\nWinner: {winner}", fontsize=14)
    plt.text(-1.5, 1, f"Winner: {winner}", fontsize=12, color='red')
    plt.text(1.2, -1, f"Winner: {winner}", fontsize=12, color='red')
    plt.show()

def user_vote():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Vote for a Candidate", font=("Arial", 14)).pack(pady=20)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM candidates")
    candidates = cursor.fetchall()
    conn.close()
    
    def cast_vote(candidate_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE candidates SET votes = votes + 1 WHERE id = %s", (candidate_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Vote cast successfully!")
        user_login()
    
    for cid, name in candidates:
        tk.Button(root, text=name, width=20, command=lambda cid=cid: cast_vote(cid)).pack(pady=5)
    
    tk.Button(root, text="Back", command=user_login).pack()

setup_db()
main_menu()
root.mainloop()
