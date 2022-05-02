from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Filters list for input string and returns list of results
def filter_vehicle_by_string(df, string):
    # filters Vehicle column for given string
    df = df[df['Vehicle: '].str.contains(string)]
    # remove the duplicates in the column and sorts in order
    df = df[["Vehicle: "]].drop_duplicates().sort_values(by=['Vehicle: '])
    # convert column results to a list
    vehicle_list = df['Vehicle: '].to_list()
    return vehicle_list


# concats the Year, Make, Model strings into one column, Vehicle
def merge_name(df):
    # make new column that concats Year, make, and Model into 1 column
    df["Vehicle: "] = (df['Year: '].astype(str) + ' '
                       + df['Make: '].astype(str) + ' '
                       + df['Model: '].astype(str)).str.replace('  ', '')
    # drop Year, make, and Model columns and return new df
    df2 = df[['Vehicle: ', 'Price: ', 'Mileage: ', 'Date: ']]
    return df2


# fixes initial data into something easy to work with
def fix_initial_data(df):
    df = df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])
    # df = df.dropna(subset=["Date: "])
    # df = df[df['Date: '] != '']
    df = df[df['Date: '].notna()]
    # df = df[df['Price: '].str.contains(',')]
    df = df.replace(',', '', regex=True)
    df['Mileage: '] = pd.to_numeric(df['Mileage: '].str.split(" ", 1).str[0], downcast="signed")
    df["Price: "] = pd.to_numeric(df["Price: "], downcast="signed")
    df = df.drop_duplicates() # in case we grabbed same vehicle entry more than once
    return df


def update(data):
    # clear list box
    list1.delete(0, END)

    # add to list box
    for item in data:
        list1.insert(END, item)


# update entry box with listbox clicked
def fillout(e):
    # delete what is in the entry box
    entry1.delete(0, END)
    # add clicked list item to entry box
    entry1.insert(0, list1.get(ACTIVE))


def check(e):
    # get what is typed
    typed = entry1.get()
    if typed == '':
        data = vehicle_list
    else:
        data = []
        for item in vehicle_list:
            if typed.lower() in item.lower():
                data.append(item)
    update(data)


def getGraphDF(vehicle_name, mileage_range, history):
    if mileage_range == "":
        mileage_range = "0-300000"
    df3 = df2
    df3 = df3[df3['Vehicle: '].str.contains(vehicle_name)]
    df3["Mileage: "] = pd.to_numeric(df3["Mileage: "], downcast="signed")
    df3["Date: "] = pd.to_datetime(df3["Date: "])
    mrl = mileage_range.split('-')
    mr1 = pd.to_numeric(mrl[0])
    mr2 = pd.to_numeric(mrl[1])

    df3 = df3[df3['Mileage: '].between(mr1, mr2)]
    return df3


# will take search parameters and make graph
def click(e):
    # displayLabel.config(text="")
    entry3.insert(END, '30')

    vehicle_name = entry1.get()
    mileage_range = entry2.get()
    history = entry2.get()

    df3 = getGraphDF(vehicle_name, mileage_range, history)

    # plot graph
    figure2 = plt.Figure(figsize=(5, 4), dpi=100)

    if mileage_range == "":
        mileage_range = "0-300000"
    ax2 = figure2.add_subplot(111)
    line2 = FigureCanvasTkAgg(figure2, root)
    line2.get_tk_widget().grid(row=1, column=3, rowspan=10,)
    df3 = df3[['Date: ', 'Price: ']].groupby('Date: ').mean()
    df3.plot(kind='line', legend=False, ax=ax2, color='orange', fontsize=10)
    ax2.set_title(str(vehicle_name) + " (" + str(mileage_range) + " miles)")

    # displayLabel.config(text = str(df3))
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry3.insert(END, '30')


if __name__ == '__main__':

    df = pd.read_csv("./mainy_df.csv")
    df2 = df.astype(str)
    df2 = fix_initial_data(df2)
    df2 = merge_name(df2)
    df2 = df2[df2["Date: "].str.contains("nan")==False]
    print(df2)

    # make Tkinter window
    root = Tk()
    root.title('Used Vehicle Price History Tool')
    root.geometry("1000x600")

    # labels
    label1 = Label(root, text="Vehicle Search", font=("Helvetica", 14), fg="grey")
    label1.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
    label2 = Label(root, text="Mileage Range", font=("Helvetica", 14), fg="grey")
    label2.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
    label3 = Label(root, text="History (days)", font=("Helvetica", 14), fg="grey")
    label3.grid(row=4, column=0, columnspan=1, padx=10, pady=10)

    displayLabel = Label(root)
    displayLabel.grid(row=1, column=3, rowspan=5)

    # entry bars
    entry1 = Entry(root, font=("Helvetica", 14), width=25)
    entry1.grid(row=1, column=1)
    entry2 = Entry(root, font=("Helvetica", 14), width=25)
    entry2.grid(row=3, column=1)
    entry3 = Entry(root, font=("Helvetica", 14), width=25)
    entry3.insert(END, '30')
    entry3.grid(row=4, column=1)

    # search vehicle list
    list1 = Listbox(root, width=30, height=10, font=("Helvetica", 15))
    list1.grid(row=2, column=1)

    # search button
    button1 = Button(root, text="Search", command=lambda: click(ACTIVE), width=10)
    button1.grid(row=5, column=1)

    # list of all vehicles
    vehicle_list = filter_vehicle_by_string(df2, "")
    update(vehicle_list)

    # Create click on item and put into search functionality
    list1.bind("<<ListboxSelect>>", fillout)
    # create binding on entry box
    entry1.bind("<KeyRelease>", check)

    root.mainloop()
