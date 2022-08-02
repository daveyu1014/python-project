# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 15:04:25 2022

@author: dave7
"""
import yfinance as yf
import tkinter as tk
import pandas as pd
from bs4 import BeautifulSoup
import pandas_datareader as pdr
import datetime, requests
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from pandastable import Table



def get_soup(url):
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    }
    resp=requests.get(url,headers=headers)
    resp.encoding='utf-8'
    
    if resp.status_code == 200:
        soup=BeautifulSoup(resp.text, 'lxml')
        return soup
    return None

def time():
    now = datetime.datetime.now()
    dt_string = now.strftime('%Y/%m/%d %H:%M:%S')
    label2.config(text = dt_string)
    label2.after(1000,time)
    

def search():
    global symbol,canvas
    
    symbol=entry1.get() 
    clearFrame()
    try:
        df = pdr.DataReader(symbol,"yahoo")      
        df=df.drop(columns = ['Volume'])        
        figure.clear()
        figure.suptitle(symbol)
        figure.add_subplot(111).plot(df['Adj Close'])
        canvas.draw()
        toolbar.update()
        button()   
    except Exception as e:
        tk.messagebox.showerror(title='Error',message=e)
  
def clearFrame():
    for widget in f8.winfo_children():
       widget.destroy()
    
def info():
            
    url=f'https://finviz.com/quote.ashx?t={symbol}'
    soup=get_soup(url)
    if soup is not None:
        tables=soup.find(class_="snapshot-table2").find_all('td')
        title=[]
        content=[]
        datas=[]
        for i,table in enumerate(tables):           
            if i %2==0:
                title.append(table.text.strip())
            else:
                content.append(table.text.strip())
        datas.append(title)
        datas.append(content)
        info_df=pd.DataFrame(datas)
        
        win2=tk.Tk()
        win2.geometry('400x720')
        win2.title('Info')
        f = tk.Frame(win2, bg='antiquewhite')
        f.pack(fill='both', expand=1)
        table = Table(f, dataframe=info_df.transpose())
        table.show()
        table.rowheader.maxwidth = 90
        win2.mainloop()
    else:
       tk.messagebox.showinfo(title='error',message='No Data') 
    

def history():
          
    history_df=pdr.DataReader(symbol,"yahoo")[::-1]
    win3=tk.Tk()
    win3.geometry('830x600')
    win3.title('History')
    f = tk.Frame(win3, bg='antiquewhite')
    f.pack(fill='both', expand=1)
    table = Table(f, dataframe=history_df)
    table.showIndex()
    table.show()
    table.rowheader.maxwidth = 90
    win3.mainloop()
    
def financial():    
    
    stock = yf.Ticker(symbol)
    financial_df=stock.financials
    win4=tk.Tk()
    win4.geometry('1150x580')
    win4.title('Financial')
    f3 = tk.Frame(win4, bg='antiquewhite')
    f3.pack(fill='both', expand=1)
    table = Table(f3, dataframe=financial_df)
    table.showIndex()
    table.show()
    win4.mainloop()   
    
def balancesheet():
    stock = yf.Ticker(symbol)
    balance_sheet_df=stock.balance_sheet
    win5=tk.Tk()
    win5.geometry('1000x650')
    win5.title('Balance sheet')
    f4 = tk.Frame(win5, bg='antiquewhite')
    f4.pack(fill='both', expand=1)
    table = Table(f4, dataframe=balance_sheet_df)
    table.showIndex()
    table.show()
    win5.mainloop() 

def cashflow():
    stock = yf.Ticker(symbol)
    cashflow_df=stock.cashflow
    win6=tk.Tk()
    win6.geometry('950x500')
    win6.title('Cash flow')
    f5 = tk.Frame(win6, bg='antiquewhite')
    f5.pack(fill='both', expand=1)
    table = Table(f5, dataframe=cashflow_df)
    table.showIndex()
    table.show()
    win6.mainloop()   

def marketprediction():
    stock = yf.Ticker(symbol)
    recommendations_df=stock.recommendations
    win7=tk.Tk()
    win7.geometry('950x500')
    win7.title('Market Prediction')
    f6 = tk.Frame(win7, bg='antiquewhite')
    f6.pack(fill='both', expand=1)
    table = Table(f6, dataframe=recommendations_df)
    table.showIndex()
    table.show()
    win7.mainloop()  
    
def relatednews():
    url=f'https://finviz.com/quote.ashx?t={symbol}'
    soup=get_soup(url)
    news=soup.find(id="news-table").find_all('tr')
    date=[]
    title=[]
    link=[]
    related=[]
    for new in news:
        for n,news_td in enumerate(new.find_all('td')):
            if n % 2 == 0:
                date.append(news_td.text.strip())
            if n % 2 == 1:
                title.append(news_td.text.strip())
        link.append(new.find('a').get('href'))
    related.append(date)
    related.append(title)
    related.append(link)
    related_df=pd.DataFrame(related)   
    win8=tk.Tk()
    win8.geometry('1200x800')
    win8.title('Related News')
    f7 = tk.Frame(win8, bg='antiquewhite')
    f7.pack(fill='both', expand=1)
    table = Table(f7, dataframe=related_df.transpose())
    table.show()   
    win8.mainloop()   

def button():
        
    info_button = tk.Button(f8, text = 'Info', font=('Forte',16), command =info)
    info_button.pack(fill='x', anchor='s', padx=5, pady=8, ipady=5)                   
    
    history_button = tk.Button(f8, text = 'History', font=('Forte',16), command =history)
    history_button.pack(fill='x', anchor='s', padx=5, pady=8, ipady=5)  
    
    financial_button = tk.Button(f8, text = 'Financial', font=('Forte',16), command =financial)
    financial_button.pack(fill='x', anchor='s', padx=5, pady=8, ipady=5)  
    
    balancesheet_button = tk.Button(f8, text = 'Balance Sheet', font=('Forte',16), command =balancesheet)
    balancesheet_button.pack(fill='x', anchor='s', padx=5, pady=8, ipady=5)  
    
    cashflow_button = tk.Button(f8, text = 'Cash flow', font=('Forte',16), command =cashflow)
    cashflow_button.pack(fill='x', anchor='s', padx=5, pady=8, ipady=5)  
    
    marketprediction_button = tk.Button(f8, text = 'Market Prediction', font=('Forte',16), command =marketprediction)
    marketprediction_button.pack(fill='x', anchor='s', padx=5, pady=8, ipady=5)  
    
    relatednews_button = tk.Button(f8, text = 'Related News', font=('Forte',16), command =relatednews)
    relatednews_button.pack(fill='x', anchor='s', padx=5, pady=8, ipady=5)   
      

win=tk.Tk()
win.geometry('1150x700')

f1=tk.Frame(win, width=250, height=720, bg='steelblue')
f2=tk.Frame(win, width=900, height=720, bg='antiquewhite')
f8=tk.Frame(f1, bg='steelblue')

f1.pack(side='left', fill='y')
f2.pack(fill='both', expand=1)
f8.pack(side='bottom')


label1=tk.Label(f1, text='Insert stock symbol:' , font=('HYGungSo-Bold', 16), bg='steelblue')
label1.pack(anchor='n', padx=10,pady=10)

entry1=tk.Entry(f1, font=('Arial Black', 22), width=10)
entry1.pack(anchor='n', padx=10,pady=5)
symbol=entry1.get() 

label3=tk.Label(f2, bg='antiquewhite')
label3.pack(side= 'top',  pady=10, ipady=400, ipadx=500 )

search_button=tk.Button(f1, text='Search', font=('Forte',16), command=search)
search_button.pack(fill='x', anchor='s', padx=10, pady=8)
        
label4=tk.Label(f1, text='Search to get stock details', font=('HYGungSo-Bold', 16), bg='steelblue')
label4.pack(fill='x', anchor='s', padx=10,)

label2=tk.Label(f1, font=('Calibri', 16, 'bold'), bg='steelblue')
label2.pack(side= 'top', anchor='s', pady=10)  
time()

figure = plt.Figure(figsize=(8,6))
figure.patch.set_facecolor('antiquewhite')
canvas = FigureCanvasTkAgg(figure, master=label3)
canvas.get_tk_widget().configure(background='antiquewhite')
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
toolbar = NavigationToolbar2Tk(canvas, label3)
    
win.mainloop()










