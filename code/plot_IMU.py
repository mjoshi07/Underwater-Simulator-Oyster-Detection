import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random

N = 50 # number of points to keep

# Variables to plot
proc1=np.full(shape=(N,), fill_value=np.nan)
proc2=np.full(shape=(N,), fill_value=np.nan)
proc3=np.full(shape=(N,), fill_value=np.nan)

fig, (ax1,ax2,ax3) = plt.subplots(3,1)

line1, = ax1.plot(proc1, 'r-')
line2, = ax2.plot(proc2, 'g-')
line3, = ax3.plot(proc3, 'b-')

# Set scales accordingly
ax1.set_ylim(0,100)
ax1.set_xlim(0,N)

ax2.set_ylim(0,100)
ax2.set_xlim(0,N)

ax3.set_ylim(0,10)
ax3.set_xlim(0,N)

def animate(i):
    # Shift all vals by one
    proc1[:-1]=proc1[1:]
    # Append new val to end/alt. fetch from csv
    proc1[-1]=random.randint(0,100)

    proc2[:-1]=proc2[1:]
    proc2[-1]=random.randint(0,100)

    proc3[:-1]=proc3[1:]
    proc3[-1]=random.randint(0,10)
    
    line1.set_ydata(proc1)
    line2.set_ydata(proc2)
    line3.set_ydata(proc3)

# interval= millisec updation
ani = FuncAnimation(fig, animate, interval = 100)
plt.show()