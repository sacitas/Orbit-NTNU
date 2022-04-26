from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import tkinter as tk
import pandas as pd
import numpy as np
import csv
import os

#---Initial values---
sp = 0
kp = 0
ti = 0
td = 0
auto = 0
man = 0


#------Main GUI code-----
root = tk.Tk()
root.title("Real Time Plot")
root.configure(background = 'light grey')
root.geometry("900x600") # Window size

plt.style.use('fivethirtyeight')


#--------Save plot function--------
def savePlot():
    plt.savefig("sacitErKjekk.png")
    
#-------Plot function to animate--------
def animate(i):
    
    #-----Reads csv file & collecting data-----
    data = pd.read_csv('PID_temp.csv')
    x = data["x"]
    dtemp0 = data["dtemp0"]
    dtemp1 = data["dtemp1"]
    dtemp2 = data["dtemp2"]
    dtemp3 = data["dtemp3"]
    dtemp4 = data["dtemp4"]

    plt.cla()
    
    plt.plot(x, dtemp0, linewidth = 1.5, label='Sensor 0')
    plt.plot(x, dtemp1, linewidth = 1.5, label='Sensor 1')
    plt.plot(x, dtemp2, linewidth = 1.5, label='Sensor 2')
    plt.plot(x, dtemp3, linewidth = 1.5, label='Sensor 3')
    plt.plot(x, dtemp4, linewidth = 1.5, label='Sensor 4')
    
    plt.ylim([0, 200])
    plt.xticks(rotation=90, ha='right', fontsize=8)
    plt.xticks(np.arange(0, len(x)+1, 30))
    plt.legend(loc='upper left', prop={'size':10})
    plt.tight_layout()

#----------------Plot window in GUI----------------
canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().place(x = 10, y = 10, width = 600, height = 400)
canvas.draw()

#------------------Animate function------------------
ani = FuncAnimation(plt.gcf(), animate, interval=500)

#-------Setting regulator values-------
def SetRegVals():  
    
    global sp, kp, ti, td, auto, man
    #-----Gets values from input fields-----
    sp = SP_ent.get()
    sp = float(sp)
    kp = kp_ent.get()
    kp = float(kp)
    ti = ti_ent.get()
    ti = float(ti)
    td = td_ent.get()
    td = float(td)
    
#-----Sets auto/manual mode from checkbox-----
    if (var0.get() == 1):
        auto = 1
    else:
        auto = 0
    #-----Gets value from input field-----
    man = man_ent.get()
    man = float(man)
    
#-----------Writes the regulator values to file-------------
    with open ('pid.conf', 'w') as f:
        f.write('%s,%s,%s,%s,%s,%s'%(sp,kp,ti,td,auto,man))

#-------Creates checkbutton-------
root.update()
var0 = tk.IntVar()
MA = tk.Checkbutton(root, text='AUTO', variable=var0, onvalue=1, offvalue=0)
MA.place(x = 670, y = 50)

#-------Creates button-------
root.update()
S_P = tk.Button(root, text = "Save plot", font = ('calibri', 12), command = lambda: savePlot())
S_P.place(x = 670, y = 90)

#-------Create input fields--------
root.update()
SP_label = tk.Label(root, text = 'SP:', font = ('calibre', 10))
SP_label.place(x = 640, y = 140)
SP_ent = tk.Entry(root)
SP_ent.insert(0, "25")
SP_ent.place(x = 670, y = 140)

root.update()
kp_label = tk.Label(root, text = 'Kp:', font = ('calibre', 10))
kp_label.place(x = 640, y = SP_label.winfo_y()+SP_label.winfo_reqwidth() + 10)
kp_ent = tk.Entry(root)
kp_ent.insert(0, "1")
kp_ent.place(x = 670, y = SP_label.winfo_y()+SP_label.winfo_reqwidth() + 10)

root.update()
ti_label = tk.Label(root, text = 'Ti:', font = ('calibre', 10))
ti_label.place(x = 640, y = kp_label.winfo_y()+kp_label.winfo_reqwidth() + 10)
ti_ent = tk.Entry(root)
ti_ent.insert(0, "0")
ti_ent.place(x = 670, y = kp_label.winfo_y()+kp_label.winfo_reqwidth() + 10)

root.update()
td_label = tk.Label(root, text = 'Td:', font = ('calibre', 10))
td_label.place(x = 640, y = ti_label.winfo_y()+ti_label.winfo_reqwidth() + 10)
td_ent = tk.Entry(root)
td_ent.insert(0, "0")
td_ent.place(x = 670, y = ti_label.winfo_y()+ti_label.winfo_reqwidth() + 10)

root.update()
man_label = tk.Label(root, text = 'Manual:', font = ('calibre', 10))
man_label.place(x = 640, y = td_label.winfo_y()+td_label.winfo_reqwidth() + 10)
man_ent = tk.Entry(root)
man_ent.insert(0, "0")
man_ent.place(x = 670, y = td_label.winfo_y()+td_label.winfo_reqwidth() + 10)

#-------Creates button-------
root.update()
SV = tk.Button(root, text = "SET", font = ('calibri', 12), command = lambda: SetRegVals())
SV.place(x = 670, y = 350)
        
   
root.mainloop()