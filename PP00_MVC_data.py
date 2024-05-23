# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:04:26 2024

@author: maxva
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy import signal

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y

order = 6
fs = 1000
cutoff = 10

#for i in range(4):
MVC = np.loadtxt("PP00_MVC.txt")[:, -1]
MVC = MVC[31000: 35800]
MVC = ((MVC-(2**16-1)/2)/32768)*1.5
t = range(0, len(MVC))
plt.plot(t, MVC)


lp = butter_lowpass_filter((MVC**2), cutoff, fs, order)
lp = np.sqrt(lp)
plt.plot(t, lp, 'k')
max_lp = np.max(lp)
arg_max = np.argmax(lp)
print('MVC =', max_lp)
#plt.plot(np.argmax(lp), max_lp, 'o', color='red')
plt.vlines(x = arg_max, ymin = -1, ymax = max_lp, color='r', linewidth=0.7)
plt.ylim(-0.8, 0.5);