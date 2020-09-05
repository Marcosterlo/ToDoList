#!/usr/bin/env python3

from tkinter import *
import pickle
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector

# Defining the connection to database
db = mysql.connector.connect(
	host="sql7.freemysqlhosting.net",
	user="sql7362581",
	passwd="Login_system20!",
	database="sql7362581"
	)

cursor = db.cursor()

# Common MySQL commands
sel_all = "SELECT content FROM todolist"
insert_command = "INSERT INTO todolist (content) VALUES ('"

#scratch of the backend

list = []

def save_list():
	cursor.execute("DELETE FROM todolist WHERE (1=1)")
	for i in list:
		cursor.execute(insert_command + str(i) + "')")
	db.commit()
   	
def load_list():
    global list
    list = []
    cursor.execute(sel_all)
    iter = cursor.fetchall()
    for i in iter:
    	list.append(i[0])
    
def add():
    new = inp.get()
    if new == "":
        messagebox.showerror("Input Error", "Type some text first!")
    else:
        list.append(new)
        save_list()
        inp.delete(0, "end")
        refresh_listbox()
    return

def delete():
    element = listbox.get("active")
    if element in list:
        confirm = messagebox.askokcancel("Deleting element", "Are you sure you want to delete '" + str(element) +"'?")
        if confirm:
            list.remove(element)
            save_list()
            refresh_listbox()
    return

def delete_all():
    global list
    confirm = messagebox.askokcancel("Deleting All", "Are you sure you want to delete everything?")
    if confirm:
        list=[]
        save_list()
        refresh_listbox()
    return

def replace():
    global list
    input = inp.get()
    replaced = listbox.get("active")
    index = listbox.curselection()[0]
    if input == "":
        messagebox.showerror("Input error", "Type some text first!")
    else:
        if replaced in list:
            confirm = messagebox.askquestion("Replacing", "Do you want to replace '" + str(replaced) + "' with '" + str(input) +"'?")
            if confirm == "yes":
                inp.delete(0, "end")
                list.remove(replaced)
                list.insert(index, input)
                save_list()
                refresh_listbox()
    return

def clear():
    inp.delete(0, "end")
    return

def refresh_listbox():
    listbox.delete(0, "end")
    for act in list:
        listbox.insert("end", act)
    return

#Graphic's part

root = Tk()
root.title("To Do List")

btn_add = ImageTk.PhotoImage(Image.open("/home/marco/.todolist/buttons/button_add.png"))
btn_del = ImageTk.PhotoImage(Image.open("/home/marco/.todolist/buttons/button_delete.png"))
btn_delall = ImageTk.PhotoImage(Image.open("/home/marco/.todolist/buttons/button_delete-all.png"))
btn_rep = ImageTk.PhotoImage(Image.open("/home/marco/.todolist/buttons/button_replace.png"))
btn_clear = ImageTk.PhotoImage(Image.open("/home/marco/.todolist/buttons/button_clear.png"))

Label(root, text="To Do List", fg="red", padx=20, pady=20, font=("", 40, "bold")).grid(row=0, column=0, columnspan=2)

Label(root, padx=4, pady=10, text="", fg="red", font=("", 20, "")).grid(row=1, column=0, columnspan=2) #It'll be used for messages

inp = Entry(root, width=30, font=("", 20, ""), bd=5)
inp.grid(row=2, column=0, padx=5, pady=10)

Button(root, padx=5, pady=10, image=btn_add, borderwidth=0, command=add).grid(row=3, column=0)
Button(root, padx=5, pady=10, image=btn_del, borderwidth=0, command=delete).grid(row=4, column=0)
Button(root, padx=5, pady=10, image=btn_delall, borderwidth=0, command=delete_all).grid(row=5, column=0)
Button(root, padx=5, pady=10, image=btn_rep, borderwidth=0, command=replace).grid(row=6, column=0)
Button(root, padx=5, pady=10, image=btn_clear, borderwidth=0, command=clear).grid(row=7, column=0)

Label(root, pady=5).grid(row=8, column=0) #spacer for the bottom of window

listbox = Listbox(root, width=30, font=("", 20, ""), selectmode=SINGLE, bd=5, height=12)
listbox.grid(row=2, column=1, rowspan=6, padx=10, pady=10)

scroll = Scrollbar(root)
scroll.grid(row=2, column=2, rowspan=6, pady=10, padx=5, sticky=N+S)

scroll2 = Scrollbar(root, orient=HORIZONTAL)
scroll2.grid(row=8, column=1, pady=10, padx=5, sticky=E+W)

listbox.config(yscrollcommand = scroll.set, xscrollcommand = scroll2.set)
scroll.config(command = listbox.yview)
scroll2.config(command = listbox.xview)

#Operative section()
load_list()

refresh_listbox()

root.mainloop()
