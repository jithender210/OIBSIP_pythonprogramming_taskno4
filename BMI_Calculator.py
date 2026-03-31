import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt
conn=sqlite3.connect("BMIdatbase.db")
cursor=conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_record(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               Name varchar(10),
               weight REAL,
               height REAL,
               bmi REAL,
               Date TEXT)''')
conn.commit()

def calculate_bmi():
    weight = weight_var.get()
    height = height_var.get()
    name=name_var.get()
    date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    if height <= 0:
        messagebox.showerror("Error", "Height must be greater than zero!")
        return

    bmi = weight / (height ** 2)
    cursor.execute("INSERT INTO bmi_record (Name, weight, height, bmi, Date) VALUES (?, ?, ?, ?, ?)", (name, weight, height, bmi, date))
    conn.commit()
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"


    entry.delete(0,tk.END)
    entry.insert(0,f"{bmi:.2f}")
    category_entry.delete(0,tk.END)
    category_entry.insert(0,category)

def view_history():
    cursor.execute("SELECT * FROM bmi_record")
    records = cursor.fetchall()
    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    for record in records:
        tk.Label(history_window, text=f"Name: {record[1]}, Weight: {record[2]} kg, Height: {record[3]} m, BMI: {record[4]:.2f}, Date: {record[5]}").pack()

def show_graph():
    data=cursor.execute("SELECT bmi ,Date FROM bmi_record WHERE Name= ?", (name_var.get(),)).fetchall()
    if not data:
        messagebox.showinfo("No Data", "No BMI records found for the given name.")
        return
    bmi=[r[0] for r in data]
    date=[r[1] for r in data]
    plt.plot(date,bmi,marker='o')
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title(f"BMI Progress for {name_var.get()}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


root = tk.Tk()
root.title("BMI Calculator")
root.geometry("300x300")
tk.Label(root,text="Name").pack()
name_var = tk.StringVar()
tk.Entry(root,textvariable=name_var).pack()

tk.Label(root, text="Weight (kg)").pack()
weight_var= tk.DoubleVar()
tk.Entry(root,textvariable=weight_var).pack()
tk.Label(root, text="Height (m)").pack()
height_var = tk.DoubleVar()
tk.Entry(root, textvariable=height_var).pack()
tk.Button(root,text="Calculate BMI", bg="blue",fg="white",command=lambda:calculate_bmi()).pack(pady=5)
entry = tk.Entry(root, width=30)
entry.pack()
tk.Label(root,text="Category").pack()
category_entry=tk.Entry(root,width=30)
category_entry.pack()

tk.Button(root,text="view history",bg="green",fg="white",command=lambda: view_history()).pack(pady=10)
tk.Button(root,text="show graph",command=lambda:show_graph()).pack()
root.mainloop()