from tkinter import *
from PIL import ImageTk, Image

import os,sys
os.chdir ("/Users/aleksejustinov/prj/metrotest/")

position=0

btnCnt=0

def btnActionPass():
  pass
btnAction=btnActionPass

def btnPosActionPass():
  pass
btnPosAction= btnPosActionPass

root=Tk()

root.geometry("480x320")
#root.attributes('-fullscreen',True)

image1 = Image.open('252Z.png')
image2 = Image.open('519Z.png')
image3 = Image.open('221Z.png')
img1=image1.resize((480,320))
img2=image2.resize((480,320))
img3=image3.resize((480,320))
bg=ImageTk.PhotoImage(img1)
imgS=ImageTk.PhotoImage(img3)

image4 = Image.open('Images/4.png')
img4 = image4.resize((118,83))
imgBtn=ImageTk.PhotoImage(img4)

image5 = Image.open('Images/5.png')
img5 = image5.resize((118,83))
imgBtn2=ImageTk.PhotoImage(img5)

image6 = Image.open('Images/6.png')
img6 = image6.resize((119,54))
imgBtn6=ImageTk.PhotoImage(img6)


image9 = Image.open('Images/9.png')
img9 = image9.resize((147,35))
imgBtn9=ImageTk.PhotoImage(img9)

image10 = Image.open('Images/10.png')
img10 = image10.resize((147,35))
imgBtn10=ImageTk.PhotoImage(img10)

label1 = Label (root, image = bg)
label1.place ( x=0, y=0)

simMode=0

def callback_myButton_Red():
    myButton.configure(image=imgBtn2,command=callback_myButton_Green)
    root.update()

    print('to_green')
    

def callback_myButton_Green():
    myButton.configure(image=imgBtn,command=callback_myButton_Red)
    root.update()

    print('to_red')


V1=37
V2=2.2
V3=3.3

#V1_edited=V1
#V2_edited=V2
#V3_edited=V3

#V1_new=V1
#V2_new=V2
#V3_new=V3
#ссылка на активный элемент
# команда записи при изменении элемента
# команда чтения активного элемента

def Settings():

    global V1,V2,V3,position #,V1_edited,V2_edited,V3_edited,V1_new,V2_new,V3_new

    V1_new=V1
    V2_new=V2
    V3_new=V3

    V1_edited=V1
    V2_edited=V2
    V3_edited=V3
    
    print("Init settings")
    
    #position=V1*10

    def s_update():
      #print("s_update3. Position={} V1_new={} V1_edited={}".format(position,V1_new,V1_edited))
   
      entry1.delete(0,last=END);
      entry1.insert(0,V1_edited)

      entry2.delete(0,last=END);
      entry2.insert(0,V2_edited)

      entry3.delete(0,last=END);
      entry3.insert(0,V3_edited)



      s.after(1000,s_update)

    def entry1_btn_Action():
      nonlocal V1_new
      global btnAction
      print("entry1_btn_Action")
      V1_new=V1_edited
      #entry1.config({"takefocus": "0"})
      s.focus_set() #s.focus()
      
    
    def entry1_Pos_Action():
      nonlocal V1_edited
      print("entry1_Pos_Action. V1_edited={}".format(V1_edited))
      V1_edited=position/10

    def entry1_focus_in(event):
      global position,btnAction,btnPosAction
      entry1.config({"background": "LightGreen"})
      btnAction=entry1_btn_Action
      btnPosAction=entry1_Pos_Action
      position=V1_new*10
      entry1.delete(0,last=END);
      entry1.insert(0,V1_new)
      print('Entry1 got focus.')


    def entry1_focus_out(event):
      nonlocal V1_edited
      global btnAction,btnPosAction
      V1_edited=V1_new
      btnAction=lambda:True
      btnPosAction=lambda:True
      entry1.config({"background": "White"})

      print('Entry1 lost focus.')

      #r=bytearray([0x00,0x00,0x00,0x08,0x00,0x00,0x00,0x8B]) #'\x00000004\x0000000E\x00000001' # enable test signal
      #import struct
      #for ii in reversed(struct.pack('d',position/10)):
       #  r.append(ii)

      #sock.send(r)

    def entry2_btn_Action():
      print("FF2")
    def entry2_focus_in(event):
      entry2.config({"background": "LightGreen"})

      print('Entry2 got focus.Send 0x8B')


    def entry2_focus_out(event):
      entry2.config({"background": "White"})
      print('Entry2 lost focus.')

    def entry3_focus_in(event):
      entry3.config({"background": "LightGreen"})
      print('Entry3 got focus.')
      CmdEmu=3

    def entry3_focus_out(event):
      entry3.config({"background": "White"})
      print('Entry3 lost focus.')
    
    def Settings_SET_Btn():
      print("Settings_SET_Btn")

      s.destroy()

    def Settings_CLR_Btn():
      s.destroy()

    s=Toplevel()
    s.geometry ('480x320')
    s['bg']='grey'
    s.overrideredirect(True)
    #s.after(5000,lambda: s.destroy())
    label1 = Label (s, image = imgS)
    label1.place ( x=0, y=0)

    myButtonS_Left= Button(s,image=imgBtn9,command=Settings_SET_Btn)
    myButtonS_Left.place( x=74, y= 260) #, width=118 , height = 83)

    myButtonS_Right= Button(s,image=imgBtn10,command=lambda: s.destroy())
    myButtonS_Right.place( x=266, y= 260) #, width=118 , height = 83)


    def PosIncPressed():
      global position
      position=position+1
      #print("pos INC  pressed. position={}".format(position))
      btnPosAction()

    myButtonPos= Button(s,text="Pos+",command=PosIncPressed)
    myButtonPos.place( x=26, y= 26) #, width=118 , height = 83)

    def PosDecPressed():
      global position
      position=position-1
      #print("pos DEC  pressed. position={}".format(position))
      btnPosAction()    

    myButtonPos= Button(s,text="Pos-",command=PosDecPressed)
    myButtonPos.place( x=26, y= 76) #, width=118 , height = 83)

    def BtnPressed():
      global btnCnt
      btnCnt=btnCnt+1
      print("btn pressed. btnCnt={}".format(btnCnt))
      btnAction()

    myButtonBtn= Button(s,text="Btn",command=BtnPressed)
    myButtonBtn.place( x=26, y= 176) #, width=118 , height = 83)

    entry1=Entry(s)
    entry1.insert(0,V1)
    entry1.bind("<FocusIn>", entry1_focus_in)
    entry1.bind("<FocusOut>", entry1_focus_out) 
   #entry1.configure('active',foreground="green")
    entry1.place(x=192,y=44,width=172,height=24)  

    
    entry2=Entry(s)
    entry2.insert(0,"222.222")
    entry2.bind("<FocusIn>", entry2_focus_in)
    entry2.bind("<FocusOut>", entry2_focus_out) 
    entry2.place(x=192,y=120,width=172,height=24)

    entry3=Entry(s)
    entry3.insert(0,"333.333")
    entry3.bind("<FocusIn>", entry3_focus_in)
    entry3.bind("<FocusOut>", entry3_focus_out) 
    entry3.place(x=192,y=196,width=172,height=24)
    s.after(1000,s_update)
     
myButton= Button(image=imgBtn,command=callback_myButton_Red)
myButton.place( x=155, y= 138) #, width=118 , height = 83)

myButton2= Button(image=imgBtn6,command=Settings)
myButton2.place( x=153, y= 234 , width=119 , height = 54)

Lmax=Label(text="001.123",bg='#222', fg='#ff0', font=10)
Lmax.place(x=75,y=35, width=80)

L=Label(text="001.123",bg='#222', fg='#ff0', font=10)
L.place(x=75,y=60, width=80)

VL=Label(text="001.123",bg='#222', fg='#ff0', font=10)
VL.place(x=75,y=85, width=80)

Fmax=Label(text="001.123",bg='#222', fg='#ff0', font=10)
Fmax.place(x=225,y=35, width=80)

F=Label(text="001.123",bg='#222', fg='#ff0', font=10)
F.place(x=225,y=60, width=80)

VF=Label(text="001.123",bg='#222', fg='#ff0', font=10)
VF.place(x=225,y=85, width=80)

Dmax=Label(text="001.123",bg='#222', fg='#ff0', font=10)
Dmax.place(x=380,y=35, width=80)

D=Label(text="001.123",bg='#222', fg='#ff0', font=10)
D.place(x=380,y=60, width=80)

VD=Label(text="001.123",bg='#222', fg='#ff0', font=10)
VD.place(x=380,y=85, width=80)



LSTRAIN=Label(text="001.123",bg='#fff', fg='#000', font=10)
LSTRAIN.place(x=290,y=150, width=105)

LDISP=Label(text="001.123",bg='#fff', fg='#000', font=10)
LDISP.place(x=290,y=205, width=105)

LDEFORMATION=Label(text="001.123",bg='#fff', fg='#000', font=10)
LDEFORMATION.place(x=290,y=260, width=105)

def update():
#  rVal=4.56789
#  Lmax.configure(text=str("{:07.3F}".format(rVal)))

  root.after(1000,update)

root.after(1000,update)

root.mainloop()