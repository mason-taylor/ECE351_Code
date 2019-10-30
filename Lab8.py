#%%
# Preliminary Setup
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

halfsize_figure = (8,3)
fullsize_figure = (16,3)

#Default figure size is smaller figure
plt.rcParams.update({'font.size': 12, 'figure.figsize': fullsize_figure})

stepsize = 0.01

#%%
def a(k):
    return np.zeros(k)

def b(k):
    bk = np.zeros(k)
    for k in range(k):
        if (k > 0):
            bk[k] = (2/(k*np.pi))*(1-np.cos(np.pi*k))
        else:
            bk[k] = 0
    return bk

ak = a(4)
bk = b(3500)


#%%
# This is may initial attempt to quickly plot a graph with the sums at each N1 value.
# I noticed this algorithm is fast and efficient since it only does the work of summing the
# highest desired number of terms, and stops whenever it reaches a certain 'milestone' and
# plots the current result.
T = 8
N1 = [1, 3, 15, 50, 150, 1500]
t = np.arange(0, 20 + stepsize, stepsize)
data = np.zeros(len(t))

plt.figure(figsize=(16,5))
plt.subplot(1,1,1)
plt.title('Fourier Series Summation for Various N')
# For every k up to the max we need, add the contributions at 
# that frequency
for k in range(max(N1)):
    for t_val in range(len(t)):
        data[t_val] += bk[k] * np.sin(2*np.pi*k*t[t_val]/T)
    # If we are at a desired value of k, we plot the current results on 
    # the existing plot.
    if k in N1:
        plt.plot(t,data)
        plt.grid(True)

#%%
# This is my approach, it only calculates the terms for a given N once,
# keeping the running sum, but still dividing the plots out into the individual 
# figures. All it does is reuse the work in creating lower level plots to create
# the higher level plots. It also allows an arbitrary number of figures with 3 
# subplots each by just adding sets of 3 terms to N

# N1 = [1, 3, 15, 50, 150, 1500, 2000, 2500, 3000]
t = np.arange(0, 20 + stepsize, stepsize)
pltcount = 0
data = np.zeros(len(t))
plt.figure(figsize=(10,10))
plt.title('Fourier Series Summation for Various N')
for k in range(max(N1)+1):
    for t_val in range(len(t)):
        data[t_val] += bk[k] * np.sin(2*np.pi*k*t[t_val]/T)
    if k in N1:
        plt.subplot(3, 1, pltcount % 3 + 1)
        if (pltcount % 3) == 0:
            plt.title('Fourier Series Summation for Various N')
        plt.grid(True)
        plt.plot(t,data)
        plt.ylabel('Plot for N=' + str(k))
        pltcount += 1
        if (pltcount % 3) == 0 or pltcount == len(N1):
            plt.show()
            if pltcount < len(N1):
                plt.figure(figsize=(10,10))
            


#%%
# This is the algorithm demonstrated during lab
for figure in [1,2]:
    plt.figure(figsize=(10,10))
    for subplot in np.arange((figure - 1)*3, figure*3):
        data = np.zeros(len(t))
        for k in range(N1[subplot]+1):
            for t_val in range(len(t)):
                data[t_val] += bk[k] * np.sin(2*np.pi*k*t[t_val]/T)
        plt.subplot(3,1,(subplot%3)+1)
        if (subplot == (figure - 1)*3): 
            plt.title('Fourier Series Summation for Various N')
        plt.grid(True)
        plt.plot(t, data)
        plt.ylabel('Plot for N=' + str(N1[subplot])) 
    plt.show() 
    
#%%

