# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 12:26:32 2022

@author: dave7
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

font1 = ("微軟正黑體", 12)
font2 = ("標楷體", 24)
font3 = ("標楷體", 14)

win = tk.Tk()
win.geometry('%dx%d+%d+%d' % (500, 600, 250, 100))
win.title("My Health ")

date=datetime.today().strftime('%Y-%m-%d')

frame1 = tk.Frame(win, width=300, height=50)
frame1.pack(fill="x",side ='top')
frame2 = tk.Frame(win, bg='#FCF3CF', width=300, height=300)
frame2.pack(fill='both', expand=1)
frame3 = tk.Frame(win, bg="#deb887", width=456, height=250)
frame3.pack(fill="x",side='bottom')
label0 = tk.Label(frame1, font=font1, bg="black", fg="white", anchor="w")
label0.pack(fill="x")

load= Image.open("IOYUuc.jpg")
render = ImageTk.PhotoImage(load)
img = tk.Label(frame2, image=render)
img.pack()

def food():
    global tree, entry1
    
    clearFrame()
    label = tk.Label(frame2, text="食物飲養", font=font2, bg='#FCF3CF', fg='#154360')
    label.grid(row=0, column=0, columnspan=2, padx=20, pady=5)
    label1 = tk.Label(frame2, text="食物名稱: ", font=font3, bg='#FCF3CF')
    label1.grid(row=1, column=0)
    entry1 = tk.Entry(frame2, bg="lightyellow", fg="black", font=font3, borderwidth=3)
    entry1.grid(row=1, column=1, pady=5)
    
    food_button = tk.Button(frame2, text="查詢", font=font3, command=nutrition_view)
    food_button.grid(row=2, column=1, pady=10)
    
    nutrition_connect() 
    tree = ttk.Treeview(frame2, column=("c1", "c2", "c3","c4", "c5", "c6","c7", "c8", "c9"), show='headings')
    
    tree.column("#1", width=80)
    tree.heading("#1", text="Name")
    tree.column("#2", width=50)
    tree.heading("#2", text="Kcal")
    tree.column("#3", width=50)
    tree.heading("#3", text="protein")
    tree.column("#4", width=50)
    tree.heading("#4", text="Fat")
    tree.column("#5", width=50)
    tree.heading("#5", text="SFA")
    tree.column("#6", width=50)
    tree.heading("#6", text="Carb")
    tree.column("#7", width=50)
    tree.heading("#7", text="sugar")
    tree.column("#8", width=50)
    tree.heading("#8", text="fiber")
    tree.column("#9", width=50)
    tree.heading("#9", text="sodium")
    
    tree.grid(row=20, pady=10,padx=5,columnspan=2)
   

def exercise():
    global tree, entry1
    
    clearFrame()
    label = tk.Label(frame2, text="運動消耗", font=font2, bg='#FCF3CF', fg='#154360')
    label.grid(row=0, column=0, columnspan=2, padx=20, pady=5)
    label1 = tk.Label(frame2, text="運動名稱: ", font=font3, bg='#FCF3CF')
    label1.grid(row=1, column=0)
    entry1 = tk.Entry(frame2, bg="lightyellow", fg="black", font=font3, borderwidth=3)
    entry1.grid(row=1, column=1, pady=5)
    exercise_button = tk.Button(frame2, text="查詢", font=font3, command=exercise_view)
    exercise_button.grid(row=4, column=1, padx=10, pady=10)

    exercise_connect() 
    tree = ttk.Treeview(frame2, column=("c1", "c2", "c3","c4", "c5", "c6"), show='headings')
    
    tree.column("#1", width=80)
    tree.heading("#1", text="運動項目")
    tree.column("#2", width=80)
    tree.heading("#2", text="熱量(Kc/Kg/Hr)")
    tree.column("#3", width=80)
    tree.heading("#3", text="40Kg/30Min")
    tree.column("#4", width=80)
    tree.heading("#4", text="50Kg/30Min")
    tree.column("#5", width=80)
    tree.heading("#5", text="60Kg/30Min")
    tree.column("#6", width=80)
    tree.heading("#6", text="70Kg/30Min")
    
    tree.grid(row=20, pady=10,padx=5,columnspan=2)      

    
def bmi():
    global entry1, entry2  
    clearFrame()
    
    label = tk.Label(frame2, text="BMI計算", font=font2, bg='#FCF3CF', fg='#154360')
    label.grid(row=0, column=3, columnspan=2, padx=20, pady=5)
    label1 = tk.Label(frame2, text="身高: ", font=font3, bg='#FCF3CF')
    label1.grid(row=1, column=0, columnspan=2)
    entry1 = tk.Entry(frame2, bg="lightyellow", fg="black", font=font3, borderwidth=3)
    entry1.grid(row=1, column=3, pady=5)
    label2 = tk.Label(frame2, text="體重: ", font=font3, bg='#FCF3CF')
    label2.grid(row=2, column=0, columnspan=2)
    entry2 = tk.Entry(frame2, bg="lightyellow", fg="black", font=font3, borderwidth=3)
    entry2.grid(row=2, column=3, pady=5)
    bmi_button = tk.Button(frame2, text="計算", font=font3, command=bmi_calculator)
    bmi_button.grid(row=4, column=3, padx=10, pady=10)
    
    
def bmi_calculator():
    text=''
    try:
        height = eval(entry1.get())
        weight = eval(entry2.get())
        bmi_number = round(weight / (height/100)**2,2)
        
        if bmi_number <= 18.4:
            text= f"Your BMI: {bmi_number}, You are underweight."
        elif bmi_number <= 24.9:
            text= f"Your BMI: {bmi_number}, You are healthy."
        elif bmi_number <= 29.9:
            text= f"Your BMI: {bmi_number}, You are over weight."
        elif bmi_number <= 34.9:
            text= f"Your BMI: {bmi_number}, You are severely over weight."
        elif bmi_number <= 39.9:
            text= f"Your BMI: {bmi_number}, You are obese."
        else:
            text= f"Your BMI: {bmi_number}, You are severely obese."
    except:
        
        tk.messagebox.showerror(title='Error', message='Please Input Correct Key')
    
    label3 = tk.Label(frame2, text=f"{text}", font=font3, bg='#FCF3CF')
    label3.grid(row=10, column=1, columnspan=5, padx=20)
    
def record():
    global entry1, entry2, entry3, tree
    
    clearFrame()
    label = tk.Label(frame2, text="我的紀錄", font=font2, bg='#FCF3CF', fg='#154360')
    label.grid(row=0, column=0, columnspan=20, padx=5, pady=5)
    label1 = tk.Label(frame2, text="我的體重: ", font=font3, bg='#FCF3CF')
    label1.grid(row=1, column=0, columnspan=2)
    entry1 = tk.Entry(frame2, bg="lightyellow", fg="black", font=font3, borderwidth=3)
    entry1.grid(row=1, column=3, pady=5)
    label2 = tk.Label(frame2, text="飲食攝取: ", font=font3, bg='#FCF3CF')
    label2.grid(row=2, column=0, columnspan=2)
    entry2 = tk.Entry(frame2, bg="lightyellow", fg="black", font=font3, borderwidth=3)
    entry2.grid(row=2, column=3, pady=5)
    label3 = tk.Label(frame2, text="運動消耗: ", font=font3, bg='#FCF3CF')
    label3.grid(row=3, column=0, columnspan=2)
    entry3 = tk.Entry(frame2, bg="lightyellow", fg="black", font=font3, borderwidth=3)
    entry3.grid(row=3, column=3, pady=5)
    record_button = tk.Button(frame2, text="儲存", font=font3, command=record_data)
    record_button.grid(row=4, column=2, columnspan=2, padx=10, pady=10)
    
    record_connect() 
    tree = ttk.Treeview(frame2, column=("c1", "c2", "c3","c4", "c5" ), show='headings')
    
    tree.column("#1", width=90)
    tree.heading("#1", text="Date")
    tree.column("#2", width=90)
    tree.heading("#2", text="Name")
    tree.column("#3", width=90)
    tree.heading("#3", text="Weight")
    tree.column("#4", width=90)
    tree.heading("#4", text="caloric intake")
    tree.column("#5", width=90)
    tree.heading("#5", text="calorie expenditure")
    
    tree.grid(row=20, pady=20,padx=10,column=0, columnspan=4)

def clearFrame():
    for widget in frame2.winfo_children():
        widget.destroy()

def nutrition_connect():

    con1 = sqlite3.connect("nutrition.db")
    cur1 = con1.cursor()
    cur1.execute("CREATE TABLE IF NOT EXISTS table1(id INTEGER PRIMARY KEY, First TEXT, Surname TEXT)")
    con1.commit()
    con1.close()

def exercise_connect():

    con1 = sqlite3.connect("exrcise.db")
    cur1 = con1.cursor()
    cur1.execute("CREATE TABLE IF NOT EXISTS table1(id INTEGER PRIMARY KEY, First TEXT, Surname TEXT)")
    con1.commit()
    con1.close()


def nutrition_view():
    clear_all()
    key=entry1.get()
    con1 = sqlite3.connect("nutrition.db")
    cur1 = con1.cursor()
    cur1.execute(f"SELECT * FROM data WHERE 樣品名稱 LIKE '%{key}%';")
    rows = cur1.fetchall()    

    for row in rows:
        #print(row) 
        tree.insert("", tk.END, values=row)        
    con1.close()
    
def exercise_view():
    clear_all()
    key=entry1.get()
    con1 = sqlite3.connect("exrcise.db")
    cur1 = con1.cursor()
    cur1.execute(f"SELECT * FROM data WHERE 運動項目 LIKE '%{key}%';")
    rows = cur1.fetchall()    
    
    for row in rows:
        #print(row) 
        tree.insert("", tk.END, values=row) 
    con1.close()

def record_connect():

    con1 = sqlite3.connect("record.db")
    cur1 = con1.cursor()
    cur1.execute("CREATE TABLE IF NOT EXISTS table1(id INTEGER PRIMARY KEY, First TEXT, Surname TEXT)")
    con1.commit()
    con1.close()

def record_data():
    clear_all()
    
    name='Dave'
    weight=entry1.get()
    Kcalintake=entry2.get()
    kcalburn=entry3.get()
    
    sqlstr = f''' INSERT INTO data(date,name,weight,Kcalintake,kcalburn)
              VALUES("{date}","{name}","{weight}","{Kcalintake}","{kcalburn}")'''
    
    con2 = sqlite3.connect("record.db")
    cursor=con2.cursor()
    cursor.execute(sqlstr)
    con2.commit()
    con2.close()
    
    record_view()

def record_view():
    clear_all()
    con2 = sqlite3.connect("record.db")
    cur2 = con2.cursor()
    cur2.execute("SELECT * FROM data;")
    rows = cur2.fetchall()    
    
    for row in rows:
        
        tree.insert("", tk.END, values=row) 
    con2.close()


def clear_all():
   for item in tree.get_children():
      tree.delete(item)

button1 = tk.Button(frame3, text="飲食熱量", font=font3, command=food, bg='#D5F5E3',border=0)
button1.grid(row=0, column=0, padx=10, pady=5)
button2 = tk.Button(frame3, text="運動燃燒", font=font3, command=exercise, bg='#D5F5E3',border=0)
button2.grid(row=0, column=1, padx=15, pady=5)
button3 = tk.Button(frame3, text="BMI值計算", font=font3, command=bmi, bg='#D5F5E3',border=0)
button3.grid(row=0, column=2, padx=15, pady=5)
button4 = tk.Button(frame3, text="我的紀錄", font=font3, command=record, bg='#D5F5E3',border=0)
button4.grid(row=0, column=3, padx=10, pady=5)




win.mainloop()

