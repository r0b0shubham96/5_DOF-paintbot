import time
#import cv2
import subprocess
import math
import os
import ast
#from cv2 import *
#from scipy import *
#from numpy import array
import func_move_bot as fmb
import var_declaration as vd
import Run_Bot as rb
import _thread
from time import sleep
import pygame
import threading


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
global base_inc
global link1_inc
global link2_inc

temp_list = []
temp_multiple=[]
temp_multiple_base=[0]
temp_multiple_link1=[0]
temp_multiple_link2=[0]
temp_multiple_axis4=[0]
temp_multiple_axis5=[0]
base_inc = 1
link1_inc = 1
link2_inc = 1
########################################################################################################################################

def runPaintBot(threadName, pins, gear_ratio, angle, time, direction):
    print("")
    # run_rb_stepper = rb.run_stepper_bot()
    # run_rb_stepper.move_stepper(pins, gear_ratio, angle, time, direction)
    fmb.stepper_run(pins, gear_ratio, angle, time, direction)

def runLinearActuator(threadName, angle, direction):
    print("")
    fmb.link1_run(abs(angle), direction, 0)

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




def wrist_up():
    global wrist_vertical_count
    print("wrist_up")
    wrist_vertical_count=wrist_vertical_count + 1
    print(wrist_vertical_count)
    temp_list.append("wrist_up")
    fmb.wrist_run(35, 0.5, vd.wrist_dir_up)

def wrist_down():
    global wrist_vertical_count
    print("wrist_down")
    print(wrist_vertical_count)
    wrist_vertical_count=wrist_vertical_count - 1
    temp_list.append("wrist_down")
    fmb.wrist_run(35, 0.5, vd.wrist_dir_down)
   
def wrist_left():
    global wrist_horizontal_count
    wrist_horizontal_count=wrist_horizontal_count - 1
    print(wrist_horizontal_count)
    print("wrist_left")
    temp_list.append("wrist_left")
    fmb.wrist_run(20, 0.33, vd.wrist_dir_left)
    
def wrist_right():
    global wrist_horizontal_count
    wrist_horizontal_count=wrist_horizontal_count + 1
    print(wrist_horizontal_count)
    print("wrist_right")
    temp_list.append("wrist_right")
    fmb.wrist_run(20, 0.33, vd.wrist_dir_right)

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

def normal1():
    b11.config(state="normal")
    b22.config(state="normal")
    b33.config(state="normal")
    b71.config(state="normal")
    b81.config(state="normal")
    #b9.config(state="normal")
    #b10.config(state="normal")

def dis1():
    b11.config(state="disabled")
    b22.config(state="disabled")
    b33.config(state="disabled")
    b71.config(state="disabled")
    b81.config(state="disabled")
    #b9.config(state="disabled")
    #b10.config(state="disabled") 

def base_single_run(inc):
    print("send")
    # temp_list.append("send")
    # global gui_last_base_value
    global base_time
    # global base_inc
    # base_inc = base_inc + inc
    # print(base_inc)
    # temp_list.append(base_inc)
    # angle = base_inc - gui_last_base_value
    # print(angle)
    time = abs(inc)/base_time
    print(time)
    if inc < 0 :
        fmb.base_run(abs(inc), time, vd.base_dir_left)
##        link2_run(angle, time, l2_dir_up)
    elif inc > 0 :
        fmb.base_run(inc, time, vd.base_dir_right)
##        link2_run(angle, time, l2_dir_down)
    # gui_last_base_value = base_inc

def link1_single_run(inc):
    print("send1")
    # temp_list.append("send1")
    # global gui_last_link1_value
    global link1_time
    # global link1_inc
    # link1_inc = link1_inc + inc
    # print(link1_inc)
    # temp_list.append(link1_inc)
    # angle = link1_inc - gui_last_link1_value
    # print(angle)
    time = abs(inc)/link1_time
    print(time)
    if inc < 0 :
        fmb.link1_run(abs(inc), vd.l1_dir_down,0)
    elif inc > 0 :
        fmb.link1_run(inc, vd.l1_dir_up,0)
    # gui_last_link1_value = link1_inc
    
def link2_single_run(inc):
    print("send2")
    # temp_list.append("send2")
    # global gui_last_link2_value
    global link2_time
    # global link2_inc
    # link2_inc = link2_inc + 1
    # print(link2_inc)
    # temp_list.append(link2_inc)
    # angle = link2_inc - gui_last_link2_value
    # print(angle)
    time = abs(inc)/link2_time
    print(time)
    if inc < 0 :
        fmb.link2_run(abs(inc), time, vd.l2_dir_down)
    elif inc > 0 :
        fmb.link2_run(inc, time, vd.l2_dir_up)
    # gui_last_link2_value = link2_inc

# global ik
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
            _thread.start_new_thread( runPaintBot, ("base_stepper", vd.base_pins, vd.base_gear, abs(base_angle), timer, base_direction))
#            if timer == 0:
#                timer = 5
            _thread.start_new_thread( runPaintBot, ("link2_stepper", vd.link2_pins, vd.link2_gear, abs(link2_angle), timer, link2_direction))
#            _thread.start_new_thread( runPaintBot, ("wrist1_stepper", vd.wrist1_pins, vd.wrist_gear, abs(wrist_angle_left), timer, wrist_left_direction))
#            _thread.start_new_thread( runPaintBot, ("wrist2_stepper", vd.wrist2_pins, vd.wrist_gear, abs(wrist_angle_right), timer, wrist_right_direction))
            print("\n\ninside for\n\n")
            sleep(timer + 1)#_thread.start_new_thread( runLinearActuator, ("link1_dc", link1_angle, link1_direction))
            #fmb.homing()  
    
    
###############Homing Function##########################
def homin():
    print("home")
    fmb.homing()



class JoystickControl:
    def __init__(self):
        self.done = False
        self.initControl()
        self.base_up_thread = threading.Thread(target=base_single_run, args=(1,), name="base_up_thread")
        self.base_down_thread = threading.Thread(target=base_single_run, args=(-1,), name="base_down_thread")
        self.link1_up_thread = threading.Thread(target=link1_single_run, args=(1,), name="link1_up_thread")
        self.link1_down_thread = threading.Thread(target=link1_single_run, args=(-1,), name="link1_down_thread")
        self.link2_up_thread = threading.Thread(target=link2_single_run, args=(1,), name="link2_up_thread")
        self.link2_down_thread = threading.Thread(target=link2_single_run, args=(-1,), name="link2_down_thread")
        self.wrist_up_thread = threading.Thread(target=wrist_up, name="wrist_up_thread")
        self.wrist_down_thread = threading.Thread(target=wrist_down, name="wrist_down_thread")
        self.wrist_left_thread = threading.Thread(target=wrist_left, name="wrist_left_thread")
        self.wrist_right_thread = threading.Thread(target=wrist_right, name="wrist_right_thread")

        self.base_up_started = False
        self.base_down_started = False
        self.link1_up_started = False
        self.link1_down_started = False
        self.link2_up_started = False
        self.link2_down_started = False
        self.wrist_up_started = False
        self.wrist_down_started = False
        self.wrist_left_started = False
        self.wrist_right_started = False
                

    def initControl(self):
        pygame.init()
        pygame.joystick.init()

        self.startJoystick()
        if not self.done:
            self.startJoystick()
        
    def startJoystick(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.done = True
                return

        joystick_count = pygame.joystick.get_count()
        if joystick_count>0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()

            hats = joystick.get_numhats()
            if hats>0:
                hat = joystick.get_hat(0)
                if hat[0]==-1:
                    if not self.base_down_thread.is_alive():
                        if self.base_down_started:
                            self.base_down_thread.run()
                        else:
                            self.base_down_thread.start()
                            self.base_down_started = True
                    # base_single_run(-1)
                elif hat[0]==1:
                    if not self.base_up_thread.is_alive():
                        if self.base_up_started:
                            self.base_up_thread.run()
                        else:
                            self.base_up_thread.start()
                            self.base_up_started = True
                    # base_single_run(1)
                if hat[1]==-1:
                    if not self.link1_down_thread.is_alive():
                        if self.link1_down_started:
                            self.link1_down_thread.run()
                        else:
                            self.link1_down_thread.start()
                            self.link1_down_started = True
                    # link1_single_run(-1)
                elif hat[1]==1:
                    if not self.link1_up_thread.is_alive():
                        if self.link1_up_started:
                            self.link1_up_thread.run()
                        else:
                            self.link1_up_thread.start()
                            self.link1_up_started = True
                    # link1_single_run(1)

            buttons = joystick.get_numbuttons()
            if buttons>5:
                link2_up_button = joystick.get_button(4)
                link2_down_button = joystick.get_button(5)
                if link2_up_button==1:
                    if not self.link2_up_thread.is_alive():
                        if self.link2_up_started:
                            self.link2_up_thread.run()
                        else:
                            self.link2_up_thread.start()
                            self.link2_up_started = True
                    # link2_single_run(1)
                elif link2_down_button==1:
                    if not self.link2_down_thread.is_alive():
                        if self.link2_down_started:
                            self.link2_down_thread.run()
                        else:
                            self.link2_down_thread.start()
                            self.link2_down_started = True
                    # link2_single_run(-1)
                wrist_left_button = joystick.get_button(2)
                wrist_right_button = joystick.get_button(1)
                if wrist_left_button==1:
                    if not self.wrist_left_thread.is_alive():
                        if self.wrist_left_started:
                            self.wrist_left_thread.run()
                        else:
                            self.wrist_left_thread.start()
                            self.wrist_left_started = True
                    # wrist_left()
                elif wrist_right_button==1:
                    if not self.wrist_right_thread.is_alive():
                        if self.wrist_right_started:
                            self.wrist_right_thread.run()
                        else:
                            self.wrist_right_thread.start()
                            self.wrist_right_started = True
                    # wrist_right()
                wrist_up_button = joystick.get_button(3)
                wrist_down_button = joystick.get_button(0)
                if wrist_up_button==1:
                    if not self.wrist_up_thread.is_alive():
                        if self.wrist_up_started:
                            self.wrist_up_thread.run()
                        else:
                            self.wrist_up_thread.start()
                            self.wrist_up_started = True
                    # wrist_up()
                elif wrist_down_button==1:
                    if not self.wrist_down_thread.is_alive():
                        if self.wrist_down_started:
                            self.wrist_down_thread.run()
                        else:
                            self.wrist_down_thread.start()
                            self.wrist_down_started = True
                    # wrist_down()

            # axes = joystick.get_numaxes()
            # if axes>=6:
            #     link2_axis = joystick.get_axis(1)
            #     axis_5 = joystick.get_axis(3)
            #     axis_4 = joystick.get_axis(4)

            #     if axis_5==-1.0:
            #         wrist_left()
            #     elif axis_5==1.0:
            #         wrist_right()
            #     if axis_4==-1.0:
            #         wrist_up()
            #     elif axis_4==1.0:
            #         wrist_down()
            #     if link2_axis==-1.0:
            #         link2_single_run(1)
            #     elif link2_axis==1.0:
            #         link2_single_run(-1)

    def exit(self):
        self.done=True
        pygame.quit()

########################################################
fmb.gpio_setup()
fmb.i2c_setup()
while 1:
    JoystickControl()