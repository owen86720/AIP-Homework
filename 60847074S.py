# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:21:36 2019

@author: Max
"""

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def Show(img,loc):
	image = ImageTk.PhotoImage(img)
	if(loc=="ori"):
		original.configure(image = image)
		original.image = image
	if(loc=="pro"):
		processed.configure(image = image)
		processed.image = image
		
def ImgAdjust(img):
	(x,y) = img.size
	#print(str(x)+','+str(y))
	if(x>500):
		y = int(y/(x/500))
		x = 500
	if(y>700):
		x = int(x/(y/700))
		y = 700
	img = img.resize((x,y), Image.ANTIALIAS)
	return img
	
def OpenFile():
	global image_file
	global filename
	global haveopen
	filename = ''
	filepath = filedialog.askopenfilename(title='Open',filetypes=[("PNG", ".png"),("JPG",".jpg"),("BMP",".bmp"),("PPM",".ppm")])
	
	#print('++'+filepath+'...')
	if(filepath==''):
		return
	haveopen = True
	filename = filepath.split('/')
	filename = filename[-1]
	image_file = Image.open(filepath)
	image_file = ImgAdjust(image_file)
	Show(image_file,"ori")
	Show(image_file,"pro")
	
def SaveFile():
	global filename
	global haveopen
	global image_file
	if(haveopen==False):
		return
	filepath = filedialog.asksaveasfilename(title='Save',initialfile=filename ,filetypes=[("PNG", ".png"),("JPG",".jpg"),("BMP",".bmp"),("PPM",".ppm")],defaultextension='.txt')
	image_file.save(filepath)

global haveopen
haveopen = False

window = tk.Tk()
window.title('AIP60847074S')
window.geometry('1200x700')

### Meun
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Open', command=OpenFile)
filemenu.add_command(label='Save', command=SaveFile)

window.config(menu=menubar)
####

### Frame
frame = tk.Frame(window)
frame.pack()

Lframe = tk.Frame(frame)
Rframe = tk.Frame(frame)
Lframe.pack(side='left',padx=20, pady=10)
Rframe.pack(side='right',padx=20, pady=10)
###

### Label
original = tk.Label(Lframe)
Ltitle = tk.Label(Lframe, text='Original' ,bg='green').pack()
original.pack()
processed = tk.Label(Rframe)
Rtitle = tk.Label(Rframe, text='Processed' ,bg='gray').pack()
processed.pack()
###

window.mainloop()
