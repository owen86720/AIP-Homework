# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:21:36 2019

@author: Max
"""

import random
from math import cos , sin , pi , sqrt , log
import tkinter as tk
from tkinter import filedialog , simpledialog
from PIL import Image, ImageTk , ImageDraw

def Show(img,loc):
    img = ImgAdjust(img)
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
    image_file = image_file.convert('L')
    Show(image_file,"ori")
    Ltitle_text.set('Original')
    Rtitle_text.set('Processed')
    
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
    Ltitle_text.set('Original')
    Rtitle_text.set('Processed')
    
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

def Gaussian():
    global haveopen
    global image_file
    pix = image_file.load()
    #output_img = image_file.copy()
    output_img = image_file
    output = output_img.load()
    if(haveopen==False):
        return

    variance = simpledialog.askfloat("Input the variance", "Variance",minvalue=0)
    
    for i in range(image_file.size[0]):
        for j in range(0,image_file.size[1],2):
            gamma = random.random()
            phi = random.random()
            #print(gamma,phi)
            z1 = variance**(1/2) * cos(2*pi*phi) * sqrt(-2*log(gamma))
            z2 = variance**(1/2) * sin(2*pi*phi) * sqrt(-2*log(gamma))
            #print(z1,z2)
            
            temp = round(z1 + pix[i,j])
            if(temp < 0):
                output[i,j] = 0
            elif(temp > 255):
                output[i,j] = 255
            else:
                output[i,j] = temp
            
            if(j+1 == image_file.size[1]):
                break
            temp = round(z2 + pix[i,j+1])
            if(temp < 0):
                output[i,j+1] = 0
            elif(temp > 255):
                output[i,j+1] = 255
            else:
                output[i,j+1] = temp
    Show(output_img,"ori")
    
    Histogram()
    
    Ltitle_text.set('Image with noise')
    Rtitle_text.set('Histogram of  Gaussian noise')
    
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
editmenu.add_command(label='Additive white Gaussian noise', command=Gaussian)

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
Ltitle_text = tk.StringVar()
Ltitle_text.set('Original')
Ltitle = tk.Label(Lframe, textvariable = Ltitle_text ,bg='green').pack()
original = tk.Label(Lframe)
original.pack()
Rtitle_text = tk.StringVar()
Rtitle_text.set('Processed')
Rtitle = tk.Label(Rframe, textvariable = Rtitle_text ,bg='gray').pack()
processed = tk.Label(Rframe)
processed.pack()
###

window.mainloop()
