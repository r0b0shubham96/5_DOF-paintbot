from tkinter import *
import time
from tkinter import ttk
from tkinter import tix
from tkinter import messagebox
import subprocess
import math
import os
import ast
import func_move_bot as fmb
import var_declaration as vd
import Run_Bot as rb
import _thread
from time import sleep

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
    #run_rb_stepper = rb.run_stepper_bot()
    #run_rb_stepper.move_stepper(pins, gear_ratio, angle, time, direction)
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
    

#This function is being invoked from openfn()
#This function loads all the information from profile file into GUI
def openpro_multiple(idx,r2):
    #print(idx) # Print the index value
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
    stopbtn.place(x=650,y=430)
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
        fmb.link1_run(abs(angle), vd.l1_dir_down, 0)
    elif angle > 0 :
        fmb.link1_run(angle, vd.l1_dir_up, 0)
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


############## Saving the vlue one by one#######################
def save_value():
    print("SAve Value")
    temp_multiple_base.append(var11.get())
    temp_multiple_link1.append(var12.get())
    temp_multiple_link2.append(var23.get())
    temp_multiple_axis4.append(var34.get())
    temp_multiple_axis5.append(var45.get())
##############################################################
    
def play():
    time.sleep(5)
    print("play")
    print(var_iteration.get())
    print(temp_multiple_base)
    print(temp_multiple_link1)
    print(temp_multiple_link2)
    print(temp_multiple_axis4)
    print(temp_multiple_axis5)
    stopbtn.place(x=650,y=430)
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

########################################################
fmb.gpio_setup()
fmb.i2c_setup()
root =Tk()
root.title("PaintBot")
root.attributes('-zoomed',True)
#######Menu Bar#############
menubar = Menu(root)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Open", command=openfn_multiple)
editmenu.add_command(label="Save", command=savefn_multiple)
editmenu.add_command(label="Close", command=lambda:root.destroy())
menubar.add_cascade(label="File", menu=editmenu)


#################################################################### Tab Generation#################################

nb=ttk.Notebook(root,width=1020, height=500)
page1=ttk.Frame(nb)
page2=ttk.Frame(nb)
nb.add(page1, text='Single')
nb.add(page2, text='Multiple')

#######################################################################################################################

###########################Page1 i.e single starts here###########################################################
C1 = Label(page1, text = "Base")
C2 = Label(page1, text = "Link 1")
C3 = Label(page1, text = "Link 2")
C4 = Label(page1, text = "Wrist up/down")
C5 = Label(page1, text = "Wrist")
C6 = Label(page1, text="left/right")
C1.config(font=("Courier", 40))
C2.config(font=("Courier", 40))
C3.config(font=("Courier", 40))
C4.config(font=("Courier", 20))
C5.config(font=("Courier", 20))
C6.config(font=("Courier", 10))
C1.grid(row=0,column=0,pady=(30,0), sticky="nsew")
C2.grid(row=2,column=0,pady=(30,0), sticky="nsew")
C3.grid(row=4,column=0,pady=(30,0), sticky="nsew")
C4.place(x=620,y=30)
C5.place(x=890,y=150)
C6.place(x=890,y=180)
left=PhotoImage(file="left.png")
right=PhotoImage(file="right.png")

########Home Button page1#######################################
home=PhotoImage(file="home1.png")
bhome=Button(page1,image=home,borderwidth=0,command=fmb.homing)
bhome.place(x=650,y=380)
########################################################

########### Right symbol button page1#########################3
ready=PhotoImage(file="ready.png")
ready=ready.subsample(2)
brea = Button(page1, image=ready,borderwidth=0,command=normal)
#brea.grid(row=2,column=0,pady=(0,0))
brea.place(x=730, y=360)
#########################################################

##############Cross Button page1#######################################3
cancel=PhotoImage(file="cancel.png")
cancel=cancel.subsample(1)
bcan = Button(page1, image=cancel,borderwidth=0,command=dis)
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
b1= Scale( page1, variable = var,from_=-90,to=90,length=300 ,troughcolor='sky blue',orient=HORIZONTAL,borderwidth=0,state=DISABLED)#,command = sel)
b2= Scale( page1, variable = var1,to=65,length=300 ,troughcolor='sky blue',orient=HORIZONTAL,borderwidth=0,state=DISABLED)
b3= Scale( page1, variable = var2,to=150,length=300 ,troughcolor='sky blue',orient=HORIZONTAL,borderwidth=0,state=DISABLED)
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
b7 = Button(page1, image=up1,borderwidth=0,state=DISABLED,command=wrist_up,repeatdelay=500, repeatinterval=100)
b8 = Button(page1, image=down1,borderwidth=0,state=DISABLED,command=wrist_down,repeatdelay=500, repeatinterval=100)
b9 = Button(page1, image=left1,borderwidth=0,state=DISABLED,command=wrist_left,repeatdelay=500, repeatinterval=100)
b10 = Button(page1, image=right1,borderwidth=0,state=DISABLED,command=wrist_right,repeatdelay=500, repeatinterval=100)
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
############################################Page2 i.e multiple starts here###########################################################
C1 = Label(page2, text = "Base")
C2 = Label(page2, text = "Link 1")
C3 = Label(page2, text = "Link 2")
C4 = Label(page2, text = "Axis 4")
C5 = Label(page2, text = "Axis 5")
C1.config(font=("Courier", 40))
C2.config(font=("Courier", 40))
C3.config(font=("Courier", 40))
C4.config(font=("Courier", 40))
C5.config(font=("Courier", 40))
C1.grid(row=0,column=0,pady=(0,0), sticky="nsew")
C2.grid(row=2,column=0,pady=(0,0), sticky="nsew")
C3.grid(row=4,column=0,pady=(0,0), sticky="nsew")
C4.grid(row=0,column=2, sticky="nsew")
C5.grid(row=2,column=2, sticky="nsew")

####################Home Button for page 2#############################################
home1=PhotoImage(file="home1.png")
bhome1=Button(page2,image=home1,borderwidth=0,command=fmb.homing)
bhome1.place(x=720,y=420)
###########################################################################

stop1=PhotoImage(file="stop.png")
stop1=stop1.subsample(2)
stopbtn=Button(page2,image=stop1,command=fmb.homing,borderwidth=0)
#stopbtn.place(x=650,y=480)

var_iteration=StringVar(page2)
#var.set(itr_val.get())
l1=Label(page2,text="Enter the number of iterations:")
e1=Spinbox(page2, from_=1, to=500,textvariable=var_iteration)
e1.place(x=820,y=350)
l1.place(x=610,y=350)

###############################Right Button for page 2################################
ready1=PhotoImage(file="ready.png")
ready1=ready1.subsample(2)
brea1 = Button(page2, image=ready1,borderwidth=0,command=normal1)
brea1.place(x=800, y=400)
###########################################################################

#####################Cross Button for page 2##################################
cancel1=PhotoImage(file="cancel.png")
cancel1=cancel1.subsample(1)
bcan1 = Button(page2, image=cancel1,borderwidth=0,command=dis1)
bcan1.place(x=900, y=400)
##################################################################

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
b11= Scale( page2, variable = var11,from_=-90,to=90,length=300 ,troughcolor='sky blue',orient=HORIZONTAL,borderwidth=0,state=DISABLED)
b22= Scale( page2, variable = var12,to=65,length=300 ,troughcolor='sky blue',orient=HORIZONTAL,borderwidth=0,state=DISABLED)
b33= Scale( page2, variable = var23,to=150,length=300 ,troughcolor='sky blue',orient=HORIZONTAL,borderwidth=0,state=DISABLED)
b11.grid(row=1,column=0,padx=30, sticky="nsew")
b22.grid(row=3,column=0,padx=30, sticky="nsew")
b33.grid(row=5,column=0,padx=30,pady=(0,10), sticky="nsew")
b71 = Scale( page2, variable = var34,from_=-30,to=30,length=300 ,troughcolor='sky blue',orient=HORIZONTAL,borderwidth=0,state=DISABLED)
b81 = Scale( page2, variable = var45,from_=-40,to=40,length=300 ,troughcolor='sky blue',orient=HORIZONTAL,borderwidth=0,state=DISABLED)
b71.grid(row=1,column=2, sticky="nsew")
b81.grid(row=3,column=2, sticky="nsew")
#################################################################################

#####################Save values button#######################################
#send_com=PhotoImage(file="send_com.png")
button5=Button(page2,text='SEND',command=save_value)
button5.place(x=800,y=380)
buttonplay=Button(page2,text='PLAY',command=play)
buttonplay.place(x=720,y=380)
##############################################################################

page2.grid_rowconfigure(0, weight=1)
page2.grid_rowconfigure(1, weight=1)
page2.grid_rowconfigure(2, weight=1)
page2.grid_rowconfigure(3, weight=1)
page2.grid_rowconfigure(4, weight=1) # For row 0
page2.grid_columnconfigure(0, weight=1) # For column 0
page2.grid_columnconfigure(1, weight=1)
page2.grid_columnconfigure(2, weight=1)
###############################################Page2 ends here####################################################################################
##################################################################################################################################################

b1.bind('<ButtonRelease-1>',base_single_run)
b2.bind('<ButtonRelease-1>',link1_single_run)
b3.bind('<ButtonRelease-1>',link2_single_run)
wso = root.winfo_screenwidth()
hso = root.winfo_screenheight()
nb.grid(row=0,column=0,sticky=NSEW)
root.geometry("1024x600+0+0")
root.config(menu=menubar)
root.mainloop()

#runPaintBot(threadName, pins, gear_ratio, angle, time, direction)