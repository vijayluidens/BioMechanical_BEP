# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:57:29 2024

@author: maxva
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

Data_list_zero = ['PP00_zero_degrees.txt',
             'PP00_five_degrees.txt']

Data_list_five = ['PP00_zero_degrees.txt',
             'PP00_five_degrees.txt']

Data_list = [Data_list_zero, Data_list_five]

print(Data_list)

X = ['0 degrees', '5 degrees']

signal_EST = []
signal_ESL = []
mean_EST = []
mean_ESL = []
rms_EST = []
rms_ESL = []
power_EST = []
power_ESL = []
CI_EST = []
CI_ESL = []

def mean(list):
    ms = 0
    for j in range(len(list)):
        ms = ms + list[j]**2
    ms = ms/(len(list))
    rms = np.sqrt(ms)
    return rms

def CI(list):
    std_dev = np.std(list)
    sample_size = len(list)
    
    # z-value for specified confidence interval
    z_value = 1.960  # Taken from table for a 95% confidence interval
     
    margin_of_error = z_value * (std_dev / np.sqrt(sample_size))
     
    return margin_of_error     
     
for k in range(len(Data_list)):
    mean_EST = []
    mean_ESL = []    
    for i in range(len(Data_list[k])):
        
        signal_EST = np.loadtxt(Data_list[k][i])[:, -1]
        signal_ESL = np.loadtxt(Data_list[k][i])[:, -2]
        if k == 0:
            if i == 0:
                signal_EST = signal_EST[106900: 340400]
                signal_ESL = signal_ESL[106900: 340400]
            elif i == 1:
                signal_EST = signal_EST[495500: 691500]
                signal_ESL = signal_ESL[495500: 691500]
        elif k == 1:
            if i == 0:
                signal_EST = signal_EST[1500000: 1875000]
                signal_ESL = signal_ESL[1500000: 1875000]
            elif i == 1:
                signal_EST = signal_EST[1916000: 2272400]
                signal_ESL = signal_ESL[1916000: 2272400]
        signal_EST = ((signal_EST-(2**16-1)/2)/32768)*1.5
        signal_ESL = ((signal_ESL-(2**16-1)/2)/32768)*1.5
        
        
        mean_EST.append(mean(signal_EST))
        mean_ESL.append(mean(signal_ESL))
        
    rms_EST.append(mean(mean_EST))
    rms_ESL.append(mean(mean_ESL))
    CI_EST.append(CI(mean_EST))
    CI_ESL.append(CI(mean_ESL))
    print(f'{k*5} degrees RMS for thoracic =', mean_EST[-1])
    print(f'{k*5} degrees RMS for lumbar =', mean_ESL[-1])
    print(CI_EST)
X_axis = np.arange(len(Data_list)) 
  
plt.bar(X_axis - 0.2, rms_EST, 0.4, label = 'ES thoracic', yerr=CI_EST) 
plt.bar(X_axis + 0.2, rms_ESL, 0.4, label = 'ES lumbar', yerr=CI_ESL) 
  
plt.xticks(X_axis, X) 
plt.xlabel("blade angle") 
plt.ylabel("mV")  
plt.legend() 
plt.show() 
    

    
   