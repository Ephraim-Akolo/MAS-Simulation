import sys
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

lax1, lax2, lax3, lax4, lax5, lax6 = None, None, None, None, None, None
sax1, sax2, sax3, sax4, sax5, sax6 = None, None, None, None, None, None
stime = None

def animation_frame(i):
    lax1.set_ydata(sax1[:i])
    lax2.set_ydata(sax2[:i])
    lax3.set_ydata(sax3[:i])
    lax4.set_ydata(sax4[:i])
    lax5.set_ydata(sax5[:i])
    lax6.set_ydata(sax6[:i])
    t = stime[:i]
    lax1.set_xdata(t)
    lax2.set_xdata(t)
    lax3.set_xdata(t)
    lax4.set_xdata(t)
    lax5.set_xdata(t)
    lax6.set_xdata(t)

def plot_graph(name, x = 100, resolution = 600, v = 1.05, v_padding = 1.2, c = 250, c_padding = 1.3, fault_v1 = 0.7, fault_c1 = 300, fault_v2 = 0.7, fault_c2 = 300, fault_v3 = 0.7, fault_c3 = 300, animation=True, fault_bar=False):
    c, fault_c1, fault_c2, fault_c3, animation, fault_bar = float(c), float(fault_c1), float(fault_c2), float(fault_c3), True if animation == "True" or animation == '1' else False, True if fault_bar == "True" or fault_bar == '1' else False
    t_start = int(0.2 * resolution)
    t_end = int(0.4 * resolution)
    cy_lim = c//2
    cy_lim = [-c, -cy_lim, 0, cy_lim, c]
    vy_lim = [-v, -fault_v1, 0, fault_v1, v]

    fault_v1 = v if c == fault_c1 else fault_v1
    fault_v2 = v if c == fault_c2 else fault_v2
    fault_v3 = v if c == fault_c3 else fault_v3
    
    fault_v1 = 0 if fault_c1 < 1 else fault_v1
    fault_v2 = 0 if fault_c2 < 1 else fault_v2
    fault_v3 = 0 if fault_c3 < 1 else fault_v3
    
    time = np.linspace(0, x, resolution)
    fig, (ax1, ax2) = plt.subplots(nrows=2)

    global lax1, lax2, lax3, lax4, lax5, lax6, sax1, sax2, sax3, sax4, sax5, sax6, stime
    sax1 = np.sin(time)*c 
    sax1[t_start:t_end] *= fault_c1/c
    lax1, *_ = ax1.plot(time[:1]/100,sax1[:1], label='phase 1')

    sax2 = np.sin(time - 2*(np.pi)/3)*c 
    sax2[t_start:t_end] *= fault_c2/c
    lax2, *_ = ax1.plot(time[:1]/100, sax2[:1], label='phase 2')

    sax3 = np.sin(time + 2*(np.pi)/3)*c
    sax3[t_start:t_end] *= fault_c3/c
    lax3, *_ = ax1.plot(time[:1]/100, sax3[:1], label='phase 3')
    # ax1.axhline(y=0, color='k')
    if fault_bar:
        ax1.axvline(x=0.198, color="red")
        ax1.axvline(x=0.402, color="red")
    ax1.legend(loc = 'lower right')
    ax1.set_ylim([-c*c_padding, c*c_padding])
    ax1.set_xlim([0, 1])
    ax1.set_ylabel("Current (A)")
    ax1.set_yticks(cy_lim)

    sax4 = np.sin(time)*v
    sax4[t_start:t_end] *= fault_v1/v
    lax4, *_ = ax2.plot(time[:1]/100, sax4[:1], label='phase 1')

    sax5 = np.sin(time - 2*(np.pi)/3)*v
    sax5[t_start:t_end] *= fault_v2/v
    lax5, *_ = ax2.plot(time[:1]/100, sax5[:1], label='phase 2')

    sax6 = np.sin(time + 2*(np.pi)/3)*v 
    sax6[t_start:t_end] *= fault_v3/v
    lax6, *_ = ax2.plot(time[:1]/100, sax6[:1], label='phase 3')
    # ax2.axhline(y=0, color='k')
    if fault_bar:
        ax2.axvline(x=0.198, color="red")
        ax2.axvline(x=0.402, color="red")
    stime = time/x
    ax2.legend(loc = 'lower right')
    ax2.set_ylim([-v*v_padding, v*v_padding])
    ax2.set_xlim([0, 1])
    ax2.set_ylabel("Voltage (pu)")
    ax2.set_yticks(vy_lim)

    plt.xlabel("time (s)")
    plt.suptitle(f"Bus {name} Fault Analysis")
    fig.canvas.manager.set_window_title("Plottings")
    if animation:
        anim = FuncAnimation(fig, func = animation_frame, frames=np.arange(0, resolution, 4), interval=100, repeat=False)
    else:
        animation_frame(resolution)
    plt.show()

if __name__ == "__main__":
      plot_graph(**dict(arg.split('=') for arg in sys.argv[1:]))