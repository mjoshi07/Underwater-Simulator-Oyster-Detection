import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import csv
import time

N = 50  # number of points to keep

# Variables to plot
proc1 = np.full(shape=(N,), fill_value=np.nan)
proc2 = np.full(shape=(N,), fill_value=np.nan)
proc3 = np.full(shape=(N,), fill_value=np.nan)
proc4 = np.full(shape=(N,), fill_value=np.nan)
proc5 = np.full(shape=(N,), fill_value=np.nan)
proc6 = np.full(shape=(N,), fill_value=np.nan)

fig, (ax, ay, az, wx, wy, wz) = plt.subplots(6, 1)

line1, = ax.plot(proc1, 'r-')
line2, = ay.plot(proc2, 'g-')
line3, = az.plot(proc3, 'b-')
line4, = wx.plot(proc4, 'm-')
line5, = wy.plot(proc5, 'y-')
line6, = wz.plot(proc6, 'c-')

# Set scales accordingly
ax.set_ylim(-.001, .001)
ax.set_xlim(0, N)
ax.set_xlabel('t')
ax.set_ylabel('ax')

ay.set_ylim(-.01, .01)
ay.set_xlim(0, N)
ay.set_xlabel('t')
ay.set_ylabel('ay')

az.set_ylim(-.1, .1)
az.set_xlim(0, N)
az.set_xlabel('t')
az.set_ylabel('az')

wx.set_ylim(-.1, .1)
wx.set_xlim(0, N)
wx.set_xlabel('t')
wx.set_ylabel('wx')

wy.set_ylim(-.1, .1)
wy.set_xlim(0, N)
wy.set_xlabel('t')
wy.set_ylabel('wy')

wz.set_ylim(-.1, .1)
wz.set_xlim(0, N)
wz.set_xlabel('t')
wz.set_ylabel('wz')

current_accels=[]
current_ang_accels=[]

def animate(i):
    first=True
    with open(r'D:\Programming\Underwater-Robotics\data\imu_sim_data\gyro_ideal.csv') as f1, open(r'D:\Programming\Underwater-Robotics\data\imu_sim_data\accel_ideal.csv') as f2:
        for y, x in zip(f1, f2):
            if(first):
                first=False
                pass
            else:
                # print("X,Y:",x,y)

                current_accels=x.split(',')
                current_ang_accels=y.split(',')

    # Shift all vals by one
    # Append new val to end- fetched from csv
                proc1[:-1] = proc1[1:]
                proc2[:-1] = proc2[1:]
                proc3[:-1] = proc3[1:]
                proc4[:-1] = proc4[1:]
                proc5[:-1] = proc5[1:]
                proc6[:-1] = proc6[1:]
               

                proc1[-1],proc2[-1],proc3[-1]=float(current_accels[0]),float(current_accels[1]),float(current_accels[2])
                proc4[-1],proc5[-1],proc6[-1]=float(current_ang_accels[0]),float(current_ang_accels[1]),float(current_ang_accels[2])
                line1.set_ydata(proc1)
                line2.set_ydata(proc2)
                line3.set_ydata(proc3)
                line4.set_ydata(proc4)
                line5.set_ydata(proc5)
                line6.set_ydata(proc6)

ani = FuncAnimation(fig, animate, interval=100)
plt.show()
