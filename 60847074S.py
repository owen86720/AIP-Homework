# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:21:36 2019

@author: Max
"""

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk , ImageDraw

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
	if(filepath==''):
		return
	haveopen = True
	filename = filepath.split('/')
	filename = filename[-1]
	image_file = Image.open(filepath)
	image_file = ImgAdjust(image_file)
	image_file = image_file.convert('L')
	Show(image_file,"ori")
	
def SaveFile():
	global filename
	global haveopen
	global image_file
	if(haveopen==False):
		return
	filepath = filedialog.asksaveasfilename(title='Save',initialfile=filename ,filetypes=[("PNG", ".png"),("JPG",".jpg"),("BMP",".bmp"),("PPM",".ppm")],defaultextension='.txt')
	image_file.save(filepath)

def Histogram():
	global haveopen
	global image_file
	if(haveopen==False):
		return
	
	### Calculate the sum of each pixel value and do the normalization
	count = [0] * 256
	pix = image_file.load()
	for i in range(image_file.size[0]):
		for j in range(image_file.size[1]):
			count[pix[i, j]] = count[pix[i, j]] + 1
	count = Normalization(count,600)
	
	### Draw the histogram
	his = Image.new("L", (510, 700), 255)
	draw = ImageDraw.Draw(his)
	for i in range(256):
		if(count[i]>0):
			draw.line([(i*2,645),(i*2,645-count[i])],fill=0,width=2)
		draw.rectangle([(i*2,650),(i*2+2,700)],fill=i)
	Show(his,"pro")

def Normalization(x,size):
	Min = min(x)
	Denominator = max(x) - Min
	for i in range(len(x)):
		x[i] = round((x[i] - Min)*size / Denominator)
	return x
		
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

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=editmenu)
editmenu.add_command(label='Histogram', command=Histogram)

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
