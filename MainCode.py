import tkinter as tk
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
load_dotenv()
db=None


db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        autocommit=True
    )


print('''Enter a choice:
             
             1. To add new stundent details
             2. To remove stundent details
             3. To update stundent details''')
choice=int(input("-> "))


if choice==1:
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
            cursor=db.cursor()
            query = "INSERT INTO student_details(name, USN, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (name_val, usn_val, Email_val))
            db.commit()
            cursor.close()

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
        
        
    except Error as e:
        messagebox.showerror("SQL ERROR: ", str(e))
    else:
        root.mainloop()


elif choice==2:
    def delete():
        
        usn_val = Usn.get().strip().upper()
        if not usn_val:
            messagebox.showerror("Validation", "USN is required")
            return
        
        try:
            cursor=db.cursor()
            query1="DELETE FROM student_details WHERE USN=%s"
            cursor.execute(query1, (usn_val,))
            db.commit()

            deleted=cursor.rowcount # -> returns 0 if no change is done in the database
            cursor.close()
            if deleted:
                messagebox.showinfo("SUCCESSFUL", f" Details deleted from the Database!")

            else:
                messagebox.showinfo("ERROR", "USN does not exist!")
                
            Usn.delete(0, tk.END)
            root.destroy()
            
        except Error as e:
            messagebox.showerror("SQL ERROR: ",str(e))
    try:
        root=tk.Tk()
        cursor=db.cursor()
        root.title("Details removal")
        tk.Label(root, text="Enter USN: ").grid(row=0, column=0)
        Usn=tk.Entry(root)
        Usn.grid(row=0,column=1)
        
        delete_Button=tk.Button(root, text="Delete", command=delete)
        delete_Button.grid(row=3, column=0, columnspan=2)
        cursor.close()
        
            
    except Error as e:
        messagebox.showerror("SQL ERROR: ", str(e))
    else:
        root.mainloop()
elif choice==3:
    def Update():
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
            cursor=db.cursor()
            query="UPDATE student_details SET name=%s, email=%s WHERE USN=%s"
            cursor.execute(query, (name_val, Email_val, usn_val))
            db.commit()
            cursor.close()
        except Error as e:
            messagebox.showerror("SQL ERROR: ", str(e))
        else:
            root.mainloop()

# connect → cursor → execute → commit → verify