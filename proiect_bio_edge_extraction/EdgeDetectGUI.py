import tkinter as tk
from tkinter import ttk
import os
import re
from urllib.request import urlopen 
from urllib.error import *
import sys
import datetime


logo = r'C:\Users\IBM_ADMIN\Desktop\Master MPI\BIO\proiect_bio_edge_extraction\logo.gif'


def callback():
    root.destroy()
    os.system("image_edge_extraction.py")
    

root = tk.Tk()
root.title("EdgeDetect")

logo = tk.PhotoImage(file=logo)

w = 300
h = 220
# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

tk.Label(root, 
         text="""Welcome to Image Edge Detection Tool""",
         font='Helvetica 9 bold',
         justify = tk.CENTER,
         padx = 60,
         pady = 10).pack()

tk.Label(root, 
         text="""Press START to perform Image Edge Detection""",
         font='Helvetica 8 bold',
         justify = tk.CENTER,
         padx = 60,
         pady = 5).pack()


w1 = tk.Label(root, image=logo).pack()

submitBtn = tk.Button(
                   text="START",
                   font='Helvetica 8 bold',
                   command=callback)
submitBtn.pack(side=tk.BOTTOM)


root.mainloop()
