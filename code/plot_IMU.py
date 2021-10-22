import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

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
line4, = wx.plot(proc1, 'm-')
line5, = wy.plot(proc2, 'y-')
line6, = wz.plot(proc3, 'c-')

# Set scales accordingly
ax.set_ylim(-10, 10)
ax.set_xlim(0, N)
ax.set_xlabel('t')
ax.set_ylabel('ax')

ay.set_ylim(-10, 10)
ay.set_xlim(0, N)
ay.set_xlabel('t')
ay.set_ylabel('ay')

az.set_ylim(-10, 10)
az.set_xlim(0, N)
az.set_xlabel('t')
az.set_ylabel('az')

wx.set_ylim(-10, 10)
wx.set_xlim(0, N)
wx.set_xlabel('t')
wx.set_ylabel('wx')

wy.set_ylim(-10, 10)
wy.set_xlim(0, N)
wy.set_xlabel('t')
wy.set_ylabel('wy')

wz.set_ylim(-10, 10)
wz.set_xlim(0, N)
wz.set_xlabel('t')
wz.set_ylabel('wz')


def animate(i):
    # Shift all vals by one
    # Append new val to end/alt. fetch from csv
    proc1[:-1] = proc1[1:]
    proc1[-1] = np.random.rand()

    proc2[:-1] = proc2[1:]
    proc2[-1] = np.random.rand()

    proc3[:-1] = proc3[1:]
    proc3[-1] = np.random.rand()

    proc4[:-1] = proc4[1:]
    proc4[-1] = np.random.rand()

    proc5[:-1] = proc5[1:]
    proc5[-1] = np.random.rand()

    proc6[:-1] = proc6[1:]
    proc6[-1] = np.random.rand()

    line1.set_ydata(proc1)
    line2.set_ydata(proc2)
    line3.set_ydata(proc3)
    line4.set_ydata(proc4)
    line5.set_ydata(proc5)
    line6.set_ydata(proc6)


# interval= millisec updation
ani = FuncAnimation(fig, animate, interval=10)
plt.show()