# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:21:36 2019

@author: Max
"""

import random
from math import cos , sin , pi , sqrt , log
import tkinter as tk
from tkinter import filedialog , simpledialog
from PIL import Image, ImageTk , ImageDraw , ImageOps
import numpy as np

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

def MakeHistogram(img):
    ### Calculate the sum of each pixel value and do the normalization
    count = [0] * 256
    pix = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            count[pix[i, j]] = count[pix[i, j]] + 1
    count = Normalization(count,600)
    
    ### Draw the histogram
    his = Image.new("L", (510, 700), 255)
    draw = ImageDraw.Draw(his)
    for i in range(256):
        if(count[i]>0):
            draw.line([(i*2,645),(i*2,645-count[i])],fill=0,width=2)
        draw.rectangle([(i*2,650),(i*2+2,700)],fill=i)
        
    return his
    
    
def Histogram():
    global haveopen
    global image_file
    if(haveopen==False):
        return
    Ltitle_text.set('Original')
    Rtitle_text.set('Processed')
    
    his = MakeHistogram(image_file)
    
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

def HarrWavelet(img,level):
    LL = Image.new('L',(int(img.size[0]/2),int(img.size[0]/2)))
    HL = LL.copy()
    LH = LL.copy()
    HH = LL.copy()
    LL_pix = LL.load()
    HL_pix = HL.load()
    LH_pix = LH.load()
    HH_pix = HH.load()
    pix = img.load()

    for i in range(0,img.size[0],2):
        for j in range(0,img.size[0],2):
            LL_pix[i/2,j/2] = int((pix[i,j] + pix[i,j+1] + pix[i+1,j] + pix[i+1,j+1])/4)

    for i in range(0,img.size[0],2):
        for j in range(0,img.size[0],2):
            HL_pix[i/2,j/2] = int((pix[i,j] - pix[i,j+1] + pix[i+1,j] - pix[i+1,j+1])/4)

    for i in range(0,img.size[0],2):
        for j in range(0,img.size[0],2):
            LH_pix[i/2,j/2] = int((pix[i,j] + pix[i,j+1] - pix[i+1,j] - pix[i+1,j+1])/4)

    for i in range(0,img.size[0],2):
        for j in range(0,img.size[0],2):
            HH_pix[i/2,j/2] = int((pix[i,j] - pix[i,j+1] - pix[i+1,j] + pix[i+1,j+1])/4)

    if(level > 1):
        A = HarrWavelet(LL,level-1)
    else:
        A = LL
    
    output = Image.new('L',(img.size[0],img.size[0]))
    N = int(img.size[0]/2-1)
    A_area = (0,0)
    HL_area = (0,N)
    LH_area = (N,0)
    HH_area = (N,N)
    output.paste(ImageOps.autocontrast(A),A_area)
    output.paste(ImageOps.autocontrast(HL),HL_area)
    output.paste(ImageOps.autocontrast(LH),LH_area)
    output.paste(ImageOps.autocontrast(HH),HH_area)
    return output

def Wavelet():
    global haveopen
    global image_file
    if(haveopen==False):
        return
    if(image_file.size[0]!=image_file.size[1]):
        if(image_file.size[0]>image_file.size[1]):
            temp = image_file.size[1]
        else:
            temp = image_file.size[0]
        temp = int(log(temp,2))
        temp = 2 ** temp
        image_file = image_file.resize((temp,temp), Image.ANTIALIAS)
        Show(image_file,'ori')
    
    level = simpledialog.askinteger("Input the level", "level",minvalue=1)
    image_file = HarrWavelet(image_file,level)
    Show(image_file,'pro')

def HistogramEqualization():
    global haveopen
    global image_file
    if(haveopen==False):
        return
    
    count = [0] * 256
    equalized = image_file.copy()
    pix = equalized.load()
    for i in range(equalized.size[0]):
        for j in range(equalized.size[1]):
            count[pix[i, j]] = count[pix[i, j]] + 1
    gmin = min(count)
    Hc = [count[0]]
    for i in range(1,255):
        Hc.append(Hc[i-1]+count[i])
    Hmin = Hc[gmin]
    T = []
    
    for i in range(255):
        T.append(round((Hc[i]-Hmin)*254/(equalized.size[1]*equalized.size[0]-Hmin)))

    for i in range(equalized.size[0]):
        for j in range(equalized.size[1]):
            pix[i,j] = T[pix[i,j]]

    ### Show image ###
    Lcombine = Image.new('RGBA', (image_file.size[0],image_file.size[1]+350), (0, 0, 0, 0))
    Rcombine = Image.new('RGBA', Lcombine.size, (0, 0, 0, 0))
    Lcombine.paste(image_file,(0,0))
    Rcombine.paste(equalized,(0,0))
    Lhis = MakeHistogram(image_file)
    Lhis = Lhis.resize((image_file.size[0],330), Image.ANTIALIAS)
    Rhis = MakeHistogram(equalized)
    Rhis = Rhis.resize((image_file.size[0],330), Image.ANTIALIAS)
    Lcombine.paste(Lhis,(0,image_file.size[1]+20))
    Rcombine.paste(Rhis,(0,image_file.size[1]+20))
    Show(Lcombine,'ori')
    Show(Rcombine,"pro")
    
def Convolution():
    global haveopen
    if(haveopen==False):
        return
    global mask
    global ask
    mask = []
    ask = tk.Toplevel()
    ask.grab_set()
    label = tk.Label(ask, text="Input mask size & value:")
    label.pack()
    
    scale = tk.Scale(ask,from_=3,to=11, orient=tk.HORIZONTAL ,showvalue=0, length=200, resolution=2.0, command=MakeMask)
    scale.pack()
    
    global mask_frame
    mask_frame = tk.Frame(ask)
    mask_frame.pack()

    submit = tk.Button(ask,text='Submit',command=DoConvolution)
    submit.pack()

def MakeMask(size):
    if(len(mask)!=0):
        for temp in mask:
            for i in temp:
                i.destroy()
    mask.clear()
    size = int(size)-1
    for i in range(size):
        temp = []
        for j in range(size):
            temp.append(tk.Entry(mask_frame,width=3))
            temp[j].grid(row=i,column=j)
        mask.append(temp)

def DoConvolution():
    global image_file
    mask_list = []
    #mask = np.arange(9)
    #mask = np.resize(mask,(3,3))
    
    for t in mask:
        temp = []
        for m in t:
            temp.append(float(m.get()))
        mask_list.append(temp)
    
    #mask_list = list(mask)
    mask_size = int((len(mask_list)-1)/2)
    pix = image_file.load()
    pixnp = np.asarray(image_file)
    #print(pixnp)
    for i in range(mask_size,image_file.size[1]-mask_size-1):
        for j in range(mask_size,image_file.size[0]-mask_size-1):
            temp = pixnp[i-mask_size:i+mask_size+1,j-mask_size:j+mask_size+1]
            pix[j,i] = int(np.sum(np.array(list(map(lambda x,y: x * y, temp,mask_list)))))
            #print(np.sum(np.array(list(map(lambda x,y: x * y, temp,mask_list))))/np.sum(np.array(mask_list)))
            #break
        #break
    Show(image_file,'pro')
    ask.destroy()


global haveopen
haveopen = False

global window
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
editmenu.add_command(label='Wavelet', command=Wavelet)
editmenu.add_command(label='Histogram equalization', command=HistogramEqualization)
editmenu.add_command(label='Convolution', command=Convolution)

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
