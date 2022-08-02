# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 23:24:00 2022

@author: dave7
"""
import datetime
import sqlite3
from tkcalendar import DateEntry
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def list_all_items():
  global connector, table
  table.delete(*table.get_children())
  all_data = connector.execute('SELECT * FROM ExpenseTracker')
  data = all_data.fetchall()
  for values in data:
     table.insert('', 'end', values=values)

#view detail for each months     
def view_expense_details():
  global table
  global date, cat, desc, amnt, MoP
  if not table.selection():
     mb.showerror('No expense selected', 'Please select an expense from the table to view its details')
  current_selected_expense = table.item(table.focus())
  values = current_selected_expense['values']
  expenditure_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))
  date.set_date(expenditure_date) ; cat.set(values[2]) ; desc.set(values[3]) ; amnt.set(values[4]) ; MoP.set(values[5])     
     
def clear_fields():
  global desc, cat, amnt, MoP, date, table
  today_date = datetime.datetime.now().date()
  cat.set('Food') ; desc.set('') ; amnt.set(0.0) ; MoP.set('Cash'); date.set_date(today_date)
  table.selection_remove(*table.selection())   

def remove_item():
  if not table.selection():
     mb.showerror('No record selected!', 'Please select a record to delete!')
     return
  current_selected_expense = table.item(table.focus())
  values_selected = current_selected_expense['values']
  surety = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')
  if surety:
     connector.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % values_selected[0])
     connector.commit()
     list_all_items()
     mb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')

def remove_all_items():
  surety = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the items from the database?', icon='warning')
  if surety:
     table.delete(*table.get_children())
     connector.execute('DELETE FROM ExpenseTracker')
     connector.commit()
     clear_fields()
     list_all_items()
     mb.showinfo('All Items deleted', 'All the items were successfully deleted')
  else:
     mb.showinfo('Ok', 'The task was aborted and no items was deleted!')

#add expenses
def add_expenses():
  global date, cat, desc, amnt, MoP
  global connector
  if not date.get() or not desc.get() or not cat.get() or not amnt.get() or not MoP.get():
     mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
  else:
     amount=(-amnt.get())
     connector.execute(
     'INSERT INTO ExpenseTracker (Date, Category, Description, Amount, ModeOfPayment, Assets) VALUES (?, ?, ?, ?, ?, ?)',
     (date.get_date(), cat.get(), desc.get(), amount, MoP.get(), 'Debit')
     )
     connector.commit()
     clear_fields()
     list_all_items()
     mb.showinfo('Expense added', 'The expense whose details you just entered has been added to the database')

#edit item
def edit_expense():
  global table
  def edit_existing_expense():
     global date, cat, desc, MoP
     global connector, table
     current_selected_expense = table.item(table.focus())
     contents = current_selected_expense['values']
     connector.execute('UPDATE ExpenseTracker SET Date = ?, Category = ?, Description = ?, Amount = ?, ModeOfPayment = ?, Assets = ? WHERE ID = ?',
                       (date.get_date(), cat.get(), desc.get(), amnt.get(), MoP.get(), contents[0]))
     connector.commit()
     clear_fields()
     list_all_items()
     mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
     edit_btn.destroy()
     return
  if not table.selection():
     mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')
     return
  view_expense_details()
  edit_btn = tk.Button(data_entry_frame, text='Edit expense', font=btn_font, width=30,
                    bg=hlb_btn_bg, command=edit_existing_expense)
  edit_btn.place(x=10, y=395)

#export to bar  
def view_balance_chart():
    window=tk.Tk()
    window.geometry('900x550')   
    window.title('View Balance Chart')
    window.resizable(False, False)       
    window.eval('tk::PlaceWindow . center')      
    cur1 = connector.cursor()
    cur1.execute("SELECT * FROM ExpenseTracker;")
    rows = cur1.fetchall() 
    
    datas=[]
    for row in rows:
        datas.append([row[1],row[2],row[4]])
    df=pd.DataFrame(datas, columns=['date','category','ammount'])    
    df2=df.sort_values(by=['date'],ascending=True)
    
    bal=0
    bal_list=[]
    for am in df2['ammount']:
        bal+=am
        bal_list.append(bal)
    
    df2['balance']=bal_list
    fig = plt.Figure(figsize=(5,5), dpi=100)
    a = fig.add_subplot(111)
    
    a.plot(df2['date'],df2['balance'])
    fig.suptitle('Balance Chart')
    
    canvas = FigureCanvasTkAgg(fig, master= window)
    canvas.draw()
    canvas.get_tk_widget().configure(background='antiquewhite')
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    
    window.mainloop() 

def view_expenses_chart():
    window=tk.Tk()
    window.geometry('900x550')   
    window.title('View Expenses Chart')
    window.resizable(False, False)       
    window.eval('tk::PlaceWindow . center')      
    cur1 = connector.cursor()
    cur1.execute("SELECT * FROM ExpenseTracker WHERE Assets == 'Debit';")
    rows = cur1.fetchall() 
    
    datas=[]
    for row in rows:
        datas.append([row[1],row[2],row[4]])
    df1=pd.DataFrame(datas, columns=['date','category','ammount'])
    df1=df1.sort_values(by=['date'],ascending=True)
    df1=(df1.groupby('category').sum())

    fig = plt.Figure(figsize=(12,8), dpi=100)
    a = fig.add_subplot(111)
    
    a.pie(df1['ammount'].abs(), autopct='%.2f%%', shadow=True, pctdistance=1.4)
    a.legend(labels=df1.index,loc = "center left")
    
    fig.suptitle('Expenses pie chart')
    canvas = FigureCanvasTkAgg(fig, master= window)
    canvas.draw()
    canvas.get_tk_widget().configure(background='antiquewhite')
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    
    window.mainloop()

#add deposit     
def add_deposit():
  global date, cat, desc, amnt, MoP
  global connector
  if not date.get() or not desc.get() or not cat.get() or not amnt.get() or not MoP.get():
     mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
  else:
     connector.execute(
     'INSERT INTO ExpenseTracker (Date, Category, Description, Amount, ModeOfPayment, Assets) VALUES (?, ?, ?, ?, ?, ?)',
     (date.get_date(), cat.get(), desc.get(), amnt.get(), MoP.get(), 'Credit')
     )
     connector.commit()
     clear_fields()
     list_all_items()
     mb.showinfo('Expense added', 'The expense whose details you just entered has been added to the database')

def balance():
    global connector
    sum_balance=connector.execute("SELECT SUM(Amount) FROM ExpenseTracker;")
    rows = sum_balance.fetchall() 
    for [row] in rows:
        return row
    
     
# Connecting to the Database
connector = sqlite3.connect("expenses.db")
cursor = connector.cursor()
connector.execute(
  'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Category TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT,  Assets TEXT)'
)
connector.commit()

# Backgrounds and Fonts
dataentery_frame_bg = '#CD6155'
buttons_frame_bg = '#F1948A'
hlb_btn_bg = '#F6DDCC'
lbl_font = ('Georgia', 13)
entry_font = 'Times 13 bold'
btn_font = ('Gill Sans MT', 13)
# Initializing the GUI window
root = tk.Tk()
root.title('Expense Tracker')
root.geometry('1200x550')
root.resizable(0, 0)
tk.Label(root, text='EXPENSE TRACKER', font=('Noto Sans CJK TC', 15, 'bold'), bg='#CD6155').pack(side='top', fill='x')
# StringVar and DoubleVar variables
cat = tk.StringVar(value='Food')
amnt = tk.DoubleVar()
desc = tk.StringVar()
MoP = tk.StringVar(value='Cash')
# Frames
data_entry_frame = tk.Frame(root, bg=dataentery_frame_bg)
data_entry_frame.place(x=0, y=30, relheight=0.95, relwidth=0.25)
buttons_frame = tk.Frame(root, bg=buttons_frame_bg)
buttons_frame.place(relx=0.25, rely=0.05, relwidth=0.75, relheight=0.21)
tree_frame = tk.Frame(root)
tree_frame.place(relx=0.25, rely=0.26, relwidth=0.75, relheight=0.74)

# Data Entry tk.Frame
tk.Label(data_entry_frame, text='Date (M/DD/YY) :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=50)
date = DateEntry(data_entry_frame, date=datetime.datetime.now().date(), font=entry_font)
date.place(x=160, y=50)
tk.Label(data_entry_frame, text='Description\t             :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=200)
tk.Entry(data_entry_frame, font=('Times 13 bold',16), width=31, text=desc).place(x=10, y=230)
tk.Label(data_entry_frame, text='Category           :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=100)
dd1 = tk.OptionMenu(data_entry_frame, cat, *['Food', 'Clothing/Beauty', 'Living', 'Transportation', 'Education', 'Entertaiment', 'Personal 3C', 'Publication fee', 'Car/Motor', 'Medical', 'Social', 'Investment', 'Salary', 'Others'])
dd1.place(x=160, y=100)     ;     dd1.configure(width=10, font=entry_font)
tk.Label(data_entry_frame, text='Amount\t             :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=150)
tk.Entry(data_entry_frame, font=entry_font, width=14, text=amnt).place(x=160, y=150)
tk.Label(data_entry_frame, text='Mode of Payment:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=280)
dd2 = tk.OptionMenu(data_entry_frame, MoP, *['Cash', 'Credit Card', 'Debit Card'])
dd2.place(x=170, y=275)     ;     dd1.configure(width=10, font=entry_font)
tk.Label(data_entry_frame, text='Balance:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=350)
tk.Label(data_entry_frame, text=f'$: {balance()}', font=lbl_font, bg=dataentery_frame_bg).place(x=170, y=350)

tk.Button(data_entry_frame, text='Add expenses', command=add_expenses, font=btn_font, width=30,
      bg=hlb_btn_bg).place(x=10, y=395)
tk.Button(data_entry_frame, text='Add deposit', command=add_deposit, font=btn_font, width=30, bg=hlb_btn_bg).place(x=10,y=450)
# Buttons' Frame
tk.Button(buttons_frame, text='Delete item', font=btn_font, width=25, bg=hlb_btn_bg, command=remove_item).place(x=30, y=5)
tk.Button(buttons_frame, text='Clear Fields', font=btn_font, width=25, bg=hlb_btn_bg,
      command=clear_fields).place(x=335, y=5)
tk.Button(buttons_frame, text='Delete All Items', font=btn_font, width=25, bg=hlb_btn_bg, command=remove_all_items).place(x=640, y=5)
tk.Button(buttons_frame, text='View Balance Chart', font=btn_font, width=25, bg=hlb_btn_bg,
      command=view_balance_chart).place(x=30, y=65)
tk.Button(buttons_frame, text='Edit Selected item', command=edit_expense, font=btn_font, width=25, bg=hlb_btn_bg).place(x=335,y=65)
tk.Button(buttons_frame, text='View Expenses Chart', font=btn_font, width=25, bg=hlb_btn_bg,
      command=view_expenses_chart).place(x=640, y=65)

# Treeview Frame
table = ttk.Treeview(tree_frame, selectmode='browse', columns=('ID', 'Date', 'Category', 'Description', 'Amount', 'Mode of Payment'))
X_Scroller = tk.Scrollbar(table, orient='horizontal', command=table.xview)
Y_Scroller = tk.Scrollbar(table, orient='vertical', command=table.yview)
X_Scroller.pack(side='bottom', fill='x')
Y_Scroller.pack(side='right', fill='y')
table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)
table.heading('ID', text='No.', anchor='center')
table.heading('Date', text='Date', anchor='center')
table.heading('Category', text='Category', anchor='center')
table.heading('Description', text='Description', anchor='center')
table.heading('Amount', text='Amount', anchor='center')
table.heading('Mode of Payment', text='Mode of Payment', anchor='center')
table.column('#0', width=0, stretch='NO')
table.column('#1', width=50, stretch='NO')
table.column('#2', width=95, stretch='NO')  # Date column
table.column('#3', width=150, stretch='NO')  # Category column
table.column('#4', width=325, stretch='NO')  # Title column
table.column('#5', width=135, stretch='NO')  # Amount column
table.column('#6', width=125, stretch='NO')  # Mode of Payment column
table.place(relx=0, y=0, relheight=1, relwidth=1)
list_all_items()

# Finalizing the GUI window
root.update()
root.mainloop()