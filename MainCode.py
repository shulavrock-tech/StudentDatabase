import tkinter as tk
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
load_dotenv()
db=None
cursor=None

db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        autocommit=True
    )
def submit():
    name_val = name.get().strip()
    usn_val = Usn.get().strip().upper()
    Email_val=email.get().strip()
    if not name_val:
        messagebox.showerror("Validation", "Name is required")
        return
    if not usn_val:
        messagebox.showerror("Validation", "USN is required")
        return
    if not Email_val:
        messagebox.showerror("Validation", "Email is mandatory")
        return
    try:
        query = "INSERT INTO student_details(name, USN, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (name_val, usn_val, Email_val))
        db.commit()

        messagebox.showinfo("Success", "Student successfully added into the database!")
        name.delete(0, tk.END)
        Usn.delete(0, tk.END)
        email.delete(0, tk.END)        
    except Error as e:
        messagebox.showerror("SQL ERROR", str(e))
try:
    cursor=db.cursor()
    root=tk.Tk()
    root.title("Student Entry Form")
    tk.Label(root, text="Enter Name:").grid(row=0, column=0)
    name=(tk.Entry(root))
    name.grid(row=0, column=1)

                
    tk.Label(root, text="Enter USN: "). grid(row=1, column=0)
    Usn=(tk.Entry(root))
    Usn.grid(row=1, column=1)
    cursor.execute("SELECT USN, name FROM student_details")
    USN_Check= cursor.fetchall()
    USN_dict={row[0]:row[1] for row in USN_Check}
    if str(Usn) in USN_dict.keys():
        messagebox.showinfo("Duplicate USN", f"This USN belongs to {USN_dict[Usn]}")
            


    tk.Label(root, text="Enter email (mandatory): ").grid(row=2,column=0)
    email=(tk.Entry(root))
    email.grid(row=2, column=1)


    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=3, column=0, columnspan=2)


    result_label = tk.Label(root, text="")
    result_label.grid(row=4, column=0, columnspan=2)

    root.mainloop()
    
except Error as e:
    messagebox.showerror("SQL ERROR: ", str(e))

finally:
    if cursor is not None:
        cursor.close()
    if db is not None:
        db.close()


# connect → cursor → execute → commit → verify