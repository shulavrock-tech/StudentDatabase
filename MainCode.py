from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
load_dotenv()
db=None
cursor=None
try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        autocommit=True
    )
    cursor=db.cursor()
    name=input("Enter your name: ").strip()
    while True:
        USN=(input("Enter your USN: ").strip()).upper()
        cursor.execute("SELECT USN, name FROM student_details")
        USN_Check= cursor.fetchall()
        USN_dict={row[0]:row[1] for row in USN_Check}
        if USN in USN_dict.keys():
            print(f"This USN belongs to {USN_dict[USN]}")
            name=input("Enter your name: ").strip()
            continue
        break
    while True:
        email=input("Enter your email(Mandatory): ").strip()
        if email=='' or "@" not in email:
            print("Email cannot be blank and must contain '@'")
            continue
        break
    query='''
    insert INTO student_details(name, USN, email)
    VALUES(%s,%s,%s)
    '''
    cursor.execute(query, (name, USN, email))
    db.commit()
    print("Student Successfully Added into Database!")
except Error as e:
    print("SQL ERROR: ",e)
finally:
    if cursor is not None:
        cursor.close()
    if db is not None:
        db.close()
# connect → cursor → execute → commit → verify