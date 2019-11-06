#%%
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy

def custom_fft(x, fs, clean):
    N = len( x ) # find the length of the signal
    X_fft = scipy.fftpack.fft ( x ) # perform the fast Fourier transform (fft)
    X_fft_shifted = scipy.fftpack.fftshift( X_fft ) # shift zero frequency components
    freq = np.arange ( - N /2 , N /2) * fs / N  # compute the frequencies for the output
    X_mag = np.abs( X_fft_shifted ) / N # compute the magnitudes of the signal
    X_phi = np.angle ( X_fft_shifted ) # compute the phases of the signal
    for i in range(len(X_phi)):
        if (np.abs(X_mag[i]) < 1e-10 and clean):
            X_phi[i] = 0
    return (freq, X_mag, X_phi)

#This function runs the fft and plots the results in the desired format
def freq_analysis_plot(x,t,fs,cleanfft,zoomed_range,figuresize,title,xlabels,ylabels):
    (freq, x_mag, x_phase) = custom_fft(x, fs, cleanfft) 
    plt.figure(figsize=figuresize)
    for i in range(1,7):
        if i == 2: continue
        plt.subplot(3, 1 if i==1 else 2, i)
        if i == 1:
            plt.title(title)
            plt.xlabel('t (s)')
            plt.plot(t,x)
        else:
            plt.stem ( freq , x_mag if i < 5 else x_phase, use_line_collection=True) 
            if (i-1) % 2 == 0: 
                plt.ylabel(ylabels[int((i-1)/2 - 1)])
            if i > 4: 
                plt.xlabel(xlabels[i-5])
            if i % 2 == 0: 
                plt.xlim(zoomed_range)
        plt.grid(True)
    plt.show()

def b(k):
    b_k = np.zeros(k)
    for k in range(1,k):
            b_k[k] = (2/(k*np.pi))*(1-np.cos(np.pi*k))
    return b_k
    
bk = b(16)
fs = 100
stepsize = 1/fs
t = np.arange(0, 2, stepsize)
titles = ['cos(2*pi*t)', '5sin(2*pi*t)', '2cos(4*pi*t-2) + (sin(12*pi*t+3))^2', 'Fourier Approximation of Square Wave']

#Loop and perform all the plotting for the lab
for i in range(0,7):
    z_range = [-2,2]
    if i % 3 == 0 and i < 6:
        data = np.cos(2*np.pi*t)
    elif i % 3 == 1 and i < 6:
        data = 5*np.sin(2*np.pi*t)
    elif i < 6:
        data = 2*np.cos(4*np.pi*t-2)+ (np.sin(12*np.pi*t + 3))**2
        z_range = [-15,15]
    else:
        t = np.arange(0, 16, stepsize)
        data = np.zeros(len(t))
        for k in range(16):
            data += bk[k] * np.sin(2*np.pi*k*t/8)
    freq_analysis_plot(data,t,fs,i>2,z_range,(10,16),titles[i%3] if i < 6 else titles[3],['Full Spectrum (Hz)', 'Zoomed (Hz)'], ['Magnitude', 'Phase'])

# %%
