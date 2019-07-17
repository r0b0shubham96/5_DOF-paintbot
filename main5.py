from tkinter import * 
import tkinter as tk
import time
#import cv2
from tkinter import ttk
from tkinter import tix
from tkinter import messagebox
import subprocess
import math
import os
import ast
#from cv2 import *
#from scipy import *
#from numpy import array
#from PIL import Image, ImageTk
#from tkinter import ttk
import func_move_bot as fmb
import var_declaration as vd
import Run_Bot as rb
import _thread
import threading
import serial
from time import sleep


global MOTION_AFTER
MOTION_AFTER = 5

global wrist_vertical_count
wrist_vertical_count = 0
global wrist_horizontal_count
wrist_horizontal_count = 0

global gui_last_base_value
gui_last_base_value = 0

global base_time
base_time = 10

global gui_last_link1_value
gui_last_link1_value = 0

global link1_time
link1_time = 2

global gui_last_link2_value
gui_last_link2_value = 0
global link2_time
link2_time = 10

global temp_list
global temp_multiple
global temp_multiple_base
global temp_multiple_link1
global temp_multiple_link2
global temp_multiple_axis4
global temp_multiple_axis5

temp_list = []
temp_multiple=[]
temp_multiple_base=[0]
temp_multiple_link1=[0]
temp_multiple_link2=[0]
temp_multiple_axis4=[0]
temp_multiple_axis5=[0]

########################################################################################################################################

def runPaintBot(threadName, pins, gear_ratio, angle, time, direction):
    print("")
    print(threadName)
    # run_rb_stepper = rb.run_stepper_bot()
    # run_rb_stepper.move_stepper(pins, gear_ratio, angle, time, direction)
    fmb.stepper_run(pins, gear_ratio, angle, time, direction)

def runLinearActuator(threadName, angle, direction):
    print("")
    fmb.link1_run(abs(angle), direction, 0)

# def relay_ON():
    

############################################################################################################################################3

#For Checking if the filename which is being saved is not already existing in our profile directory
#This function will prompt user that file name already exists and to select the new one
def check_multiple(s,r1):
    print('check')
    path='profiles_multiple'
    profil=[]
    files = os.listdir(path)
    for name in files:
        profil.append(name) # Listing all our profiles from its folder into profil list
    for i in range(len(profil)):
        if ('Profile-%s'%s) == (profil[i].replace(' ', '')[:-4]):
            print('check')
            messagebox.showinfo("Message", "File Already exists")
            r1.destroy()
            savefn_multiple()
            
    
#Whenever the user will click on Save Button this function will be called
def savefn_multiple():
    print('##################################################')
    temp_multiple.append(temp_multiple_base)
    temp_multiple.append(temp_multiple_link1)
    temp_multiple.append(temp_multiple_link2)
    temp_multiple.append(temp_multiple_axis4)
    temp_multiple.append(temp_multiple_axis5)
    fil=open("profiles_multiple/profile.txt","w")
    fil.write(str(temp_multiple))
    r1=Tk()
    w = r1.winfo_reqwidth()
    h = r1.winfo_reqheight()
    ws = r1.winfo_screenwidth()
    hs = r1.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    r1.geometry('+%d+%d' % (x, y))
    r1.title("Profile")
    l1=Label(r1,text="Enter the name of your profile:")
    var=StringVar(r1)
    e1=Spinbox(r1, from_=1, to=100,textvariable=var)
    b1=Button(r1,text="Save",command=lambda:[(print(e1.get())),check_multiple(e1.get(),r1),(fil.close()),(os.rename('profiles_multiple/profile.txt','profiles_multiple/Profile-%s.txt'%e1.get())),(r1.destroy())])
    b2=Button(r1,text="Exit",command=lambda:r1.destroy())
    l1.grid(row=0,column=0)
    e1.grid(row=1,column=0)
    b1.grid(row=2,column=1)
    b2.grid(row=2,column=2)
    r1.mainloop()
    
global ik
ik=1
#This function is being invoked from openfn()
#This function loads all the information from profile file into GUI
def openpro_multiple(idx,r2):
    #print(idx) # Print the index value
    clear()
    path='profiles_multiple'
    profil=[]
    files = os.listdir(path)
    for name in files:
        profil.append(name)
    print(profil[idx])
    with open("profiles_multiple/%s"%profil[idx])as file:
        prolist=ast.literal_eval(file.read())
    print("Prolist")
    print(prolist)
    #stopbtn.place(x=650,y=430)
    base_array=[]
    link1_array=[]
    link2_array=[]
    axis4_array=[]
    axis5_array=[]
    global temp_multiple_base
    global temp_multiple_link1
    global temp_multiple_link2
    global temp_multiple_axis4
    global temp_multiple_axis5
    temp_multiple_base=prolist[0]
    temp_multiple_link1=prolist[1]
    temp_multiple_link2=prolist[2]
    temp_multiple_axis4=prolist[3]
    temp_multiple_axis5=prolist[4]
    wrist_array=[]
    f = tk.Frame(subframe,background='slate gray')
    f.pack(side=LEFT, fill=Y)
    global ik
    print("ik",ik)
    Label(f,text=temp_multiple_base[ik:],bg='slate gray',fg='gray90').pack(side=TOP)
    
    Label(f,text=temp_multiple_link1[ik:],bg='slate gray',fg='gray90').pack(side=TOP)
    
    Label(f,text=temp_multiple_link2[ik:],bg='slate gray',fg='gray90').pack(side=TOP)
    Label(f,text=temp_multiple_axis4[ik:],bg='slate gray',fg='gray90').pack(side=TOP)
    Label(f,text=temp_multiple_axis5[ik:],bg='slate gray',fg='gray90').pack(side=TOP)
    ik=ik+1
    root.title(" Profile Name - %s"%profil[idx].replace(' ', '')[:-4]) # Changing the name of the main GUI so that user can know which Profile is being used
    r2.destroy()
    
# For deletion of profile which user see fit to delete        
def deletepro_multiple(idx,r2):
    path='profiles_multiple'
    profil=[]
    files = os.listdir(path)
    for name in files:
        profil.append(name)
    print(profil[idx])
    os.remove("profiles_multiple/%s"%profil[idx]) # Removing that file from profile directory
    r2.destroy()
    openfn_multiple()

#This function is invoked when Open button is pressed in the GUI
#It loads the profiles in a list from the directory and then make them as buttons so that user can easily access each profile 
def openfn_multiple():
    r2=Tk()
    w = r2.winfo_reqwidth()
    h = r2.winfo_reqheight()
    ws = r2.winfo_screenwidth()
    hs = r2.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    r2.geometry('+%d+%d' % (x, y))
    r2.title("Profile")
    path='profiles_multiple'
    profil=[]
    files = os.listdir(path)
    for name in files:
        if name == 'profile.txt':
            os.remove("profiles_multiple/profile.txt")
        else:
            profil.append(name)
    print(profil)
    siz=len(profil)
    h=1
    for k in range(len(profil)):
        #print(k)
        j= profil[k].replace(' ', '')[:-4]
        b=Button(r2,text=j,command=lambda idx= k:openpro_multiple(idx,r2),borderwidth=5).grid(row=h,column=0,sticky=(E,W),padx=(10,10),pady=(10,10))
        d=Button(r2,text='Delete',command=lambda idx= k:deletepro_multiple(idx,r2),borderwidth=5).grid(row=h,column=1,sticky=(E,W),padx=(10,10),pady=(10,10))
        #btn_list.append(b)
        h=h+1
    l1=Label(r2,text="Select the profile you want to open:")
    b2=Button(r2,text="Exit",width=15,command=lambda:r2.destroy(),borderwidth=5)
    l1.grid(row=0,column=0)
    b2.grid(row=h,column=0,padx=(10,0),pady=(10,10))
    r2.mainloop()
#########################################################################################################################################




def wrist_right():
    global wrist_vertical_count
    print("wrist_up")
    wrist_vertical_count=wrist_vertical_count + 1
    print(wrist_vertical_count)
    temp_list.append("wrist_up")
    fmb.wrist_run(5, 0.5 , vd.wrist_dir_up)

def wrist_left():
    global wrist_vertical_count
    print("wrist_down")
    print(wrist_vertical_count)
    wrist_vertical_count=wrist_vertical_count - 1
    temp_list.append("wrist_down")
    fmb.wrist_run(5, 0.5 , vd.wrist_dir_down)
   
def wrist_up():
    global wrist_horizontal_count
    wrist_horizontal_count=wrist_horizontal_count - 1
    print(wrist_horizontal_count)
    print("wrist_left")
    temp_list.append("wrist_left")
    fmb.wrist_run(10, 1, vd.wrist_dir_left)
    
def wrist_down():
    global wrist_horizontal_count
    wrist_horizontal_count=wrist_horizontal_count + 1
    print(wrist_horizontal_count)
    print("wrist_right")
    temp_list.append("wrist_right")
    fmb.wrist_run(10, 1, vd.wrist_dir_right)
def normal():
    b1.config(state="normal")
    b2.config(state="normal")
    b3.config(state="normal")
    b7.config(state="normal")
    b8.config(state="normal")
    b9.config(state="normal")
    b10.config(state="normal")

def dis():
    b1.config(state="disabled")
    b2.config(state="disabled")
    b3.config(state="disabled")
    b7.config(state="disabled")
    b8.config(state="disabled")
    b9.config(state="disabled")
    b10.config(state="disabled")
    
def base_single_run(self):
    print("send")
    temp_list.append("send")
    global gui_last_base_value
    global base_time
    print(var.get())
    temp_list.append(var.get())
    angle = var.get() - gui_last_base_value
    print(angle)
    time = abs(angle)/base_time
    print(time)
    if angle < 0 :
        fmb.base_run(abs(angle), time, vd.base_dir_left)
##        link2_run(angle, time, l2_dir_up)
    elif angle > 0 :
        fmb.base_run(angle, time, vd.base_dir_right)
##        link2_run(angle, time, l2_dir_down)
    gui_last_base_value = var.get()
    
def link1_single_run(self):
    print("send1")
    temp_list.append("send1")
    global gui_last_link1_value
    global link1_time
    print(var1.get())
    temp_list.append(var1.get())
    angle = var1.get() - gui_last_link1_value
    print(angle)
    time = abs(angle)/link1_time
    print(time)
    if angle < 0 :
        fmb.link1_run(abs(angle), vd.l1_dir_down,0)
    elif angle > 0 :
        fmb.link1_run(angle, vd.l1_dir_up,0)
    gui_last_link1_value = var1.get()
    
def link2_single_run(self):
    print("send2")
    temp_list.append("send2")
    global gui_last_link2_value
    global link2_time
    print(var2.get())
    temp_list.append(var2.get())
    angle = var2.get() - gui_last_link2_value
    print(angle)
    time = abs(angle)/link2_time
    print(time)
    if angle < 0 :
        fmb.link2_run(abs(angle), time, vd.l2_dir_down)
    elif angle > 0 :
        fmb.link2_run(angle, time, vd.l2_dir_up)
    gui_last_link2_value = var2.get()

ik=1
############## Saving the vlue one by one#######################
def save_value():
    global temp_multiple
    global temp_multiple_base
    global temp_multiple_link1
    global temp_multiple_link2
    global temp_multiple_axis4
    global temp_multiple_axis5
    
    print("SAve Value")
    temp_multiple_base.append(var11.get())
    temp_multiple_link1.append(var12.get())
    temp_multiple_link2.append(var23.get())
    temp_multiple_axis4.append(var34.get())
    temp_multiple_axis5.append(var45.get())
    print(temp_multiple_base)
    print(temp_multiple_link1)
    print(temp_multiple_link2)
    print(temp_multiple_axis4)
    print(temp_multiple_axis5)
    f = tk.Frame(subframe,background='slate gray')
    f.pack(side=LEFT, fill=Y)
    global ik
    print("ik",ik)
    Label(f,text=temp_multiple_base[ik:],bg='slate gray',fg='gray90').pack(side=TOP)
    
    Label(f,text=temp_multiple_link1[ik:],bg='slate gray',fg='gray90').pack(side=TOP)
    
    Label(f,text=temp_multiple_link2[ik:],bg='slate gray',fg='gray90').pack(side=TOP)
    Label(f,text=temp_multiple_axis4[ik:],bg='slate gray',fg='gray90').pack(side=TOP)
    Label(f,text=temp_multiple_axis5[ik:],bg='slate gray',fg='gray90').pack(side=TOP)
    ik=ik+1

def clear():
    global temp_multiple
    global temp_multiple_base
    global temp_multiple_link1
    global temp_multiple_link2
    global temp_multiple_axis4
    global temp_multiple_axis5
    print("Clear")
    for child in subframe.winfo_children():
        child.destroy()
    temp_multiple.clear()
    temp_multiple_base.clear()
    temp_multiple_link1.clear()
    temp_multiple_link2.clear()
    temp_multiple_axis4.clear()
    temp_multiple_axis5.clear()
    temp_multiple=[]
    temp_multiple_base=[]
    temp_multiple_link1=[]
    temp_multiple_link2=[]
    temp_multiple_axis4=[]
    temp_multiple_axis5=[]
    temp_multiple_base=[0]
    temp_multiple_link1=[0]
    temp_multiple_link2=[0]
    temp_multiple_axis4=[0]
    temp_multiple_axis5=[0]
    global ik
    ik=1

##############################################################
    
def play():
    global temp_multiple
    global temp_multiple_base
    global temp_multiple_link1
    global temp_multiple_link2
    global temp_multiple_axis4
    global temp_multiple_axis5
    time.sleep(5)
    print("play")
    print(var_iteration.get())
    print(temp_multiple_base)
    print(temp_multiple_link1)
    print(temp_multiple_link2)
    print(temp_multiple_axis4)
    print(temp_multiple_axis5)
    #stopbtn.place(x=650,y=430)
    for j in range(int(var_iteration.get())):
        for i in range(1,len(temp_multiple_base)):
            base_angle = temp_multiple_base[i] - temp_multiple_base[i - 1]
            if (base_angle >= 0):
                base_direction = vd.base_dir_left
            else:
                base_direction = vd.base_dir_right
            
            link2_angle = temp_multiple_link2[i] - temp_multiple_link2[i - 1]
            if (link2_angle >= 0):
                link2_direction = vd.l2_dir_up
            else:
                link2_direction = vd.l2_dir_down
            
            link1_angle = temp_multiple_link1[i] - temp_multiple_link1[i-1]
            if (link1_angle >= 0):
                link1_direction = vd.l1_dir_up
            else:
                link1_direction = vd.l1_dir_down
            
            wrist_angle_right = ((temp_multiple_axis4[i] - temp_multiple_axis4[i-1]) + (temp_multiple_axis5[i] - temp_multiple_axis5[i-1]))
            if (wrist_angle_right >= 0):
                wrist_right_direction = vd.wrist1_right_dir_up
            else:
                wrist_right_direction = vd.wrist1_right_dir_down
            
            wrist_angle_left = ((temp_multiple_axis4[i] - temp_multiple_axis4[i-1]) - (temp_multiple_axis5[i] - temp_multiple_axis5[i-1]))
            if (wrist_angle_left >= 0):
                wrist_left_direction = vd.wrist2_left_dir_up
            else:
                wrist_left_direction = vd.wrist2_left_dir_down
                
            print("\nbase_angle:")
            print(base_angle)
            
            print("\nbase_direction:")
            print(base_direction)
            
            print("\nlink2_angle:")
            print(link2_angle)
            
            print("\nlink2_direction:")
            print(link2_direction)
            
            print("\nlink1_angle:")
            print(link1_angle)
            
            print("\nlink1_direction:")
            print(link1_direction)
            
            print("\nwrist_angle_right:")
            print(wrist_angle_right)
            
            print("\nwrist_right_direction:")
            print(wrist_right_direction)
            
            print("\nwrist_angle_left:")
            print(wrist_angle_left)
            
            print("\nwrist_left_direction:")
            print(wrist_left_direction)
            
            timer = abs(base_angle)/8
            if timer == 0:
                timer = 5
    #        for j in range(int(var_iteration.get())):

            # relay_on()
            _thread.start_new_thread( runPaintBot, ("base_stepper", vd.base_pins, vd.base_gear, abs(base_angle), timer, base_direction))
#            if timer == 0:
#                timer = 5
            _thread.start_new_thread( runPaintBot, ("link2_stepper", vd.link2_pins, vd.link2_gear, abs(link2_angle), timer, link2_direction))
            _thread.start_new_thread( runPaintBot, ("wrist1_stepper", vd.wrist1_pins, vd.wrist_gear, abs(wrist_angle_left), timer, wrist_left_direction))
            _thread.start_new_thread( runPaintBot, ("wrist2_stepper", vd.wrist2_pins, vd.wrist_gear, abs(wrist_angle_right), timer, wrist_right_direction))
            print("\n\ninside for\n\n")
            # relay_off()
            sleep(timer + 1)#_thread.start_new_thread( runLinearActuator, ("link1_dc", link1_angle, link1_direction))
            #fmb.homing()  
    
    
def start_play_thread(event):
    print("play_thread")
    global play_thread
    play_thread = threading.Thread(target=play)
    play_thread.daemon = True
    # progressbar.start()
    play_thread.start()
    root.after(20, check_play_thread)

def check_play_thread():
    if play_thread.is_alive():
        root.after(20, check_play_thread)
    # else:
        # progressbar.stop()
###############Homing Function##########################
def homin():
    # relay_off()
    print("home")
    fmb.homing()



def pause_motion():
    file6 = open("pause.txt", "w")
    file6.write(str(0))
    file6.close()



def play_motion():
    print("play")
    with open("/home/pi/Documents/new-paint-bot/pause.txt") as file:
        pa=ast.literal_eval(file.read()) #This whole things helps in working of pause and resume control of GUI
    if str(pa)=='0':
        print("0")
        file6 = open("pause.txt", "w")
        file6.write(str(1))
        file6.close()
    elif str(pa)=='1':
        print("p")
        start_play_thread(None)

########################################################
fmb.gpio_setup()
fmb.i2c_setup()
root =Tk()
root.title("PaintBot") 
root.attributes('-zoomed',True)


#################################################################### Tab Generation#################################

nb=ttk.Notebook(root,width=1020, height=500)
page1=tk.Frame(nb,background='slate gray')
page2=tk.Frame(nb)
nb.add(page1, text='Single')
nb.add(page2, text='Multiple')

#######################################################################################################################

###########################Page1 i.e single starts here###########################################################
C1 = Label(page1, text = "Base",bg='slate gray',fg='gray90')
C2 = Label(page1, text = "Link 1",bg='slate gray',fg='gray90')
C3 = Label(page1, text = "Link 2",bg='slate gray',fg='gray90')
C4 = Label(page1, text = "Wrist up/down",bg='slate gray',fg='orange')
C5 = Label(page1, text = "Wrist",bg='slate gray',fg='orange')
C6 = Label(page1, text="left/right",bg='slate gray',fg='orange')
C1.config(font=("Calibri", 30))
C2.config(font=("Helvetica", 30))
C3.config(font=("Helvetica", 30))
C4.config(font=("Helvetica", 20))
C5.config(font=("Helvetica", 20))
C6.config(font=("Helvetica", 10))
C1.grid(row=0,column=0,pady=(30,0), sticky="nsew")
C2.grid(row=2,column=0,pady=(30,0), sticky="nsew")
C3.grid(row=4,column=0,pady=(30,0), sticky="nsew")
left=PhotoImage(file="left.png")
right=PhotoImage(file="right.png")

########Home Button page1#######################################
home=PhotoImage(file="home1.png")
bhome=Button(page1,activebackground='slate gray',highlightbackground="slate gray",image=home,borderwidth=0,bg='slate gray',command=homin)
bhome.place(x=650,y=380)
########################################################

########### Right symbol button page1#########################3
ready=PhotoImage(file="ready.png")
ready=ready.subsample(2)
brea = Button(page1, activebackground='slate gray',highlightbackground="slate gray",image=ready,borderwidth=0,bg='slate gray',command=normal)
#brea.grid(row=2,column=0,pady=(0,0))
brea.place(x=730, y=360)
#########################################################

##############Cross Button page1#######################################3
cancel=PhotoImage(file="cancel.png")
cancel=cancel.subsample(1)
bcan = Button(page1, activebackground='slate gray',highlightbackground="slate gray",image=cancel,borderwidth=0,bg='slate gray',command=dis)
#brea.grid(row=2,column=0,pady=(0,0))
bcan.place(x=830, y=360)
####################################################################

##############Variables defined for sliders page 1######################
var = IntVar()
var.set(0)
var1 = IntVar()
var2 = IntVar()
#################################################################

###############Sliders for page1#######################
b1= Scale( page1, highlightbackground="slate gray",font='bold 13',activebackground='slate gray',variable = var,from_=-90,to=90,bg='slate gray',length=300 ,troughcolor='sky blue',orient=HORIZONTAL,borderwidth=0,state=DISABLED)#,command = sel)
b2= Scale( page1, highlightbackground="slate gray",font='bold 13',activebackground='slate gray',variable = var1,to=65,length=300 ,bg='slate gray',troughcolor='sky blue',orient=HORIZONTAL,borderwidth=0,state=DISABLED)
b3= Scale( page1, highlightbackground="slate gray",font='bold 13',activebackground='slate gray',variable = var2,to=150,length=300 ,bg='slate gray',troughcolor='sky blue',orient=HORIZONTAL,borderwidth=0,state=DISABLED)
b1.grid(row=1,column=0,padx=30, sticky="nsew")
b2.grid(row=3,column=0,padx=30, sticky="nsew")
b3.grid(row=5,column=0,padx=30, sticky="nsew")
#############################################


############# Axis4 and Axis 5 Buttons##########################
up=PhotoImage(file="up.png")
down=PhotoImage(file="down.png")
up1=up.subsample(1)
down1=down.subsample(1)
left1=left.subsample(1)
right1=right.subsample(1)
b7 = Button(page1, activebackground='slate gray',highlightbackground="slate gray",image=up1,borderwidth=0,state=DISABLED,command=wrist_up,repeatdelay=500, repeatinterval=100,bg='slate gray')
b8 = Button(page1, activebackground='slate gray',highlightbackground="slate gray",image=down1,borderwidth=0,state=DISABLED,command=wrist_down,repeatdelay=500, repeatinterval=100,bg='slate gray')
b9 = Button(page1, activebackground='slate gray',highlightbackground="slate gray",image=left1,borderwidth=0,state=DISABLED,command=wrist_left,repeatdelay=500, repeatinterval=100,bg='slate gray')
b10 = Button(page1, activebackground='slate gray',highlightbackground="slate gray",image=right1,borderwidth=0,state=DISABLED,command=wrist_right,repeatdelay=500, repeatinterval=100,bg='slate gray')
b7.place(x=700,y=60)
b8.place(x=700,y=200)
b9.place(x=622,y=128)
b10.place(x=780,y=128)
#################################################################

page1.grid_rowconfigure(0, weight=1)
page1.grid_rowconfigure(1, weight=1)
page1.grid_rowconfigure(2, weight=1)
page1.grid_rowconfigure(3, weight=1)
page1.grid_rowconfigure(4, weight=1)
page1.grid_rowconfigure(5, weight=1)# For row 0
page1.grid_columnconfigure(0, weight=1) # For column 0
page1.grid_columnconfigure(1, weight=1)
page1.grid_columnconfigure(2, weight=1)



#######################################Page1 ends here##################################################################################

######################################################################################################################
frame1=tk.Frame(page2,bd=5,background='slate gray')
frame1.pack(side=LEFT,anchor=NW,fill=Y)
frame3=tk.Frame(page2,bd=5,background='slate gray')
frame3.pack(side=LEFT,expand=True,fill=BOTH)
frame2=tk.Frame(frame3,bd=5,background='slate gray')#,relief="groove")
frame2.pack(side=TOP,fill=X)

frameplay=tk.Frame(frame3,background='slate gray')
frameplay.pack(side=TOP)



#<<<<<<< HEAD
#framecv=tk.Frame(frame3,bd=5,background='slate gray')
#framecv.pack(side=LEFT,anchor=W)
#canvas1=Canvas(framecv,width=550,height=170,background='slate gray')
#canvas1.pack(side=LEFT)#,expand=True,fill=BOTH)

frame4=tk.Frame(frame3,bd=5,background='slate gray')
frame4.pack(side=BOTTOM,anchor=E)

############################################Page2 i.e multiple starts here###########################################################
C1 = Label(frame1, text = "Base",bg='slate gray',fg='gray90')
C2 = Label(frame1, text = "Link 1",bg='slate gray',fg='gray90')
C3 = Label(frame1, text = "Link 2",bg='slate gray',fg='gray90')
C4 = Label(frame1, text = "Axis 4",bg='slate gray',fg='gray90')
C5 = Label(frame1, text = "Axis 5",bg='slate gray',fg='gray90')
C1.config(font=("Courier", 10))
C2.config(font=("Courier", 10))
C3.config(font=("Courier", 10))
C4.config(font=("Courier", 10))
C5.config(font=("Courier", 10))


####################Home Button for page 2#############################################
home1=PhotoImage(file="home1.png")
bhome1=Button(frame4,image=home1,borderwidth=0, highlightbackground="slate gray",activebackground='slate gray',bg='slate gray',command=homin)
bhome1.pack(side=TOP)
###########################################################################

stop1=PhotoImage(file="stop.png")
stop1=stop1.subsample(2)
stopbtn=Button(frame3,image=stop1,borderwidth=0, highlightbackground="slate gray",activebackground='slate gray',bg='slate gray')#,command=fmb.homing)





###############################Right Button for page 2################################
pause1=PhotoImage(file="pause.png")
pause1=pause1.subsample(1)
brea1 = Button(frame4, image=pause1,borderwidth=0,command=pause_motion, highlightbackground="slate gray",activebackground='slate gray',bg='slate gray')
brea1.pack(side=TOP)
##########################################################################

#####################Cross Button for page 2##################################
play1=PhotoImage(file="play.png")
play1=play1.subsample(1)
bcan1 = Button(frame4, image=play1,borderwidth=0,command=play_motion, highlightbackground="slate gray",activebackground='slate gray',bg='slate gray')
bcan1.pack(side=TOP)
##################################################################

# fframe = Frame(canvas1, width=300, height=300,background='slate gray')
# #fframe.pack(side=BOTTOM,expand=True,fill=BOTH,anchor=N)
# canvas1.create_window((0,0), window=fframe, anchor=NW)
# cap = cv2.VideoCapture(0)
# cap.set(3,470)
# cap.set(4,350)
# time.sleep(2)
# cap.set(15, -8.0)
# v1 = Label(canvas1)
# v1.pack(side=TOP,expand=True,fill=BOTH)#,anchor=W)

# def dddd():
#     ret, frame = cap.read()
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#     img = Image.fromarray(frame)
#     nimg = ImageTk.PhotoImage(image=img)

#     v1.n_img = nimg
#     v1.configure(image=nimg)
#     fframe.after(10, dddd)


# dddd()





######################Variables for Sliders page 2###############################3
var11 = IntVar()
var11.set(0)
var12 = IntVar()
var23 = IntVar()
var34 = IntVar()
var45 = IntVar()
var34.set(0)
var45.set(0)
#############################################################################

###################Sliders for page2###########################################
b11= Scale( frame1, variable = var11,from_=-90,to=90,length=300 ,font='bold 11',troughcolor='sky blue',bg='slate gray',orient=HORIZONTAL,borderwidth=0,highlightbackground="slate gray",activebackground='slate gray')
b22= Scale( frame1, variable = var12,to=65,length=300 ,font='bold 11',troughcolor='sky blue',bg='slate gray',orient=HORIZONTAL,borderwidth=0,highlightbackground="slate gray",activebackground='slate gray')
b33= Scale( frame1, variable = var23,to=150,length=300 ,font='bold 11',troughcolor='sky blue',bg='slate gray',orient=HORIZONTAL,borderwidth=0,highlightbackground="slate gray",activebackground='slate gray')
C1.pack(fill=Y,expand=True)
b11.pack(fill=Y,expand=True)
C2.pack(fill=Y,expand=True)
b22.pack(fill=Y,expand=True)
C3.pack(fill=Y,expand=True)
b33.pack(fill=Y,expand=True)
b71 = Scale( frame1, variable = var34,from_=-30,to=30,length=300 ,font='bold 11',troughcolor='sky blue',bg='slate gray',orient=HORIZONTAL,borderwidth=0,highlightbackground="slate gray",activebackground='slate gray')
b81 = Scale( frame1, variable = var45,from_=-40,to=40,length=300 ,font='bold 11',troughcolor='sky blue',bg='slate gray',orient=HORIZONTAL,borderwidth=0,highlightbackground="slate gray",activebackground='slate gray')
C4.pack(fill=Y,expand=True)
b71.pack(fill=Y,expand=True)
C5.pack(fill=Y,expand=True)
b81.pack(fill=Y,expand=True)
#################################################################################

#####################Save values button#######################################
var_iteration=StringVar(frame3)
#var.set(itr_val.get())
l1=Label(frame3,text="Enter the number of iterations:",bg='slate gray',fg='gray90')
l1.pack(side=LEFT)
e1=Spinbox(frame3, from_=1, to=500,textvariable=var_iteration)
e1.pack(side=LEFT)

#send_com=PhotoImage(file="send_com.png")
button5=Button(frame3,text='SEND',command=save_value, highlightbackground="slate gray",activebackground='slate gray')
button5.pack(side=RIGHT)
#button5.place(x=800,y=380)
# buttonplay=Button(frame3,text='PLAY',command=play, highlightbackground="slate gray",activebackground='slate gray')
# buttonplay.pack(side=LEFT)
#buttonplay.place(x=720,y=380)
##############################################################################








frame5=tk.Frame(frame2,bd=5,background='slate gray')
frame5.pack(side=LEFT,anchor=W,fill=X,expand=YES)
topf = tk.Frame(frame5,background='slate gray')
topf.pack(side=TOP, fill=X, expand=NO)
f = tk.Frame(topf,background='slate gray')
f.pack(side=LEFT, fill=Y)
Label(f,text=' Base Values:',bg='slate gray',fg='gray90').pack(side=TOP,anchor=W)
Label(f,text='Link1 Values:',bg='slate gray',fg='gray90').pack(side=TOP,anchor=W)
Label(f,text='Link2 Values:',bg='slate gray',fg='gray90').pack(side=TOP,anchor=W)
Label(f,text='Axis4 Values:',bg='slate gray',fg='gray90').pack(side=TOP,anchor=W)
Label(f,text='Axis5 Values:',bg='slate gray',fg='gray90').pack(side=TOP,anchor=W)

def subframeConfig(events):
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas=Canvas(topf,width=520,height=15,background='slate gray')
hbar=Scrollbar(frame5,orient=HORIZONTAL)

hbar.config(command=canvas.xview)
canvas.config(xscrollcommand=hbar.set)
canvas.pack(side=LEFT,expand=False,fill=BOTH)
hbar.pack(side=BOTTOM,fill=X)
subframe = tk.Frame(canvas,background='slate gray')
canvas.create_window((0,0), window=subframe, anchor=NW, width=1000)
subframe.bind("<Configure>", subframeConfig)
frame6=tk.Frame(frame2,bd=5,background='slate gray')
frame6.pack(side=LEFT,anchor=E,fill=Y)


Button(frame6,text="Open", command=openfn_multiple).pack(side=TOP,fill=Y,expand=TRUE)
Button(frame6,text="Save", command=savefn_multiple).pack(side=TOP,fill=Y,expand=TRUE)
Button(frame6,text="Clear",command=clear).pack(side=TOP,fill=Y,expand=TRUE)

###########################################################3
###############################################Page2 ends here####################################################################################
##################################################################################################################################################

b1.bind('<ButtonRelease-1>',base_single_run)
b2.bind('<ButtonRelease-1>',link1_single_run)
b3.bind('<ButtonRelease-1>',link2_single_run)
wso = root.winfo_screenwidth()
hso = root.winfo_screenheight()
nb.grid(row=0,column=0,sticky=NSEW)
root.geometry("1024x600+0+0")
root.mainloop()