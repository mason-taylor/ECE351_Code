#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import scipy.signal as sig
import scipy
import pandas as pd
import control as con


halfsize_figure = (8,3)
fullsize_figure = (16,8)

def make_stem ( ax ,x ,y , color ='k', style ='solid', label ='', linewidths =2.5, ** kwargs ) :
    ax.axhline ( x [0] , x [ -1] ,0 , color ='r')
    ax.vlines (x , 0 ,y , color = color , linestyles = style , label = label , linewidths = linewidths )
    ax.set_ylim ([1.05* y . min () , 1.05* y . max () ])


def custom_fft(x, fs, clean):
    N = len( x ) # find the length of the signal
    X_fft = scipy.fftpack.fft ( x ) # perform the fast Fourier transform (fft)
    X_fft_shifted = scipy.fftpack.fftshift( X_fft ) # shift zero frequency components
    freq = np.arange ( - N /2 , N /2) * fs / N  # compute the frequencies for the output
    X_mag = np.abs( X_fft_shifted ) / N # compute the magnitudes of the signal
    X_phi = np.angle ( X_fft_shifted ) # compute the phases of the signal
    for i in range(len(X_phi)):
        if (np.abs(X_mag[i]) < 5e-3 and clean):
            X_phi[i] = 0
    return (freq, X_mag, X_phi)


#%%
#This function runs the fft and plots four different ranges
def freq_analysis_plot2(x,t,fs,cleanfft,zoomed_range_low, zoomed_range_high, zoomed_range_desired,figuresize,title,xlabels,ylabels):
    (freq, x_mag, x_phase) = custom_fft(x, fs, cleanfft) 
    plt.figure(figsize=figuresize)
    plt.subplots_adjust(bottom=0.01, top=1.2)
    for i in range(1,5):
        ax = plt.subplot(4, 1, i)
        if i == 1:
            plt.title(title)
            plt.xlabel('Full Spectrum')
        make_stem(ax, freq, x_mag)
        #ax.plot(freq, x_mag)
        if i == 2:
            plt.xlim(zoomed_range_low)
            plt.xlabel(xlabels[0])
        if i == 3: 
            plt.xlim(zoomed_range_high)
            plt.xlabel(xlabels[1]) 
        if i == 4: 
            plt.xlim(zoomed_range_desired)
            plt.xlabel(xlabels[2])

        plt.grid(True)
    plt.show()

#%%
#Part 1
# We need to read in the noisy signal from the file
df = pd.read_csv('NoisySignal.csv')
t = df['0'].values
sensor_sig = df['1'].values
plt.figure(figsize = (10 , 7) )
plt.plot(t, sensor_sig)
plt.grid()
plt.title('Noisy Input Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [V]')
plt.show ()

#%%
fs = 1e6
freq_analysis_plot2(sensor_sig, t, fs, True, [0, 1.8e3], [1.8e3, 200e3], [1.7e3, 2.1e3], (10,10), 'The Noisy Signal Characteristics', ['Low Frequency Noise', 'High Frequency Noise', 'Desired Signal Band'], ['Magnitude', 'Phase'])

# %%

# These are the calculated component values
R = 3.3e3
C = 47e-9
L = 150e-3

# Bandpass transfer function for our circuit
numh = [1/(R*C), 0]
denh = [1, 1/(R*C), 1/(L*C)]

# Get the frequency response transfer function 
sys = con.TransferFunction(numh, denh)

w = np.arange(1e2, 4e5, 1)
plt.rcParams["figure.figsize"] = (10,8)

# Use Control.Bode to show the bode plots for the various ranges of interest

#Full range bode plot
fig = plt.figure()
_ = con.bode ( sys , w , dB = True , Hz = True , deg = True , Plot = True )
fig.suptitle('Full Spectrum Bode Plot')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

#Desired Frequency Attenuation
fig = plt.figure()
_ = con.bode ( sys , np.arange(1.8e3*2*np.pi, 2e3*2*np.pi), dB = True , Hz = True , deg = True , Plot = True )
fig.suptitle('Desired Frequencies Bode Plot')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

#Low Frequency Attenuation
fig = plt.figure()
_ = con.bode ( sys , np.arange(0,1.8e3*2*np.pi), dB = True , Hz = True , deg = True , Plot = True )
fig.axes[0].axvline(60,0,1, color='r')

loc = plticker.MultipleLocator(base=10)
fig.axes[0].yaxis.set_major_locator(loc)
fig.suptitle('Low Frequency Bode Plot')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

#High Frequency Attenuation
fig = plt.figure()
_ = con.bode ( sys , np.arange(2e3*2*np.pi,100e3*2*np.pi), dB = True , Hz = True , deg = True , Plot = True )
fig.axes[0].axvline(50e3,0,1, color='r')
fig.suptitle('High Frequency Bode Plot')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

#>100 Khz Attenuation
fig = plt.figure(figsize=(10,8))
_ = con.bode ( sys , np.arange(100e3*2*np.pi, 400e3*2*np.pi), dB = True , Hz = True , deg = True , Plot = True )
fig.suptitle('Excess of 100KHz Bode Plot')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# %%
(num,den) = sig.bilinear(numh,denh,fs)
y = sig.lfilter(num,den, sensor_sig)

plt.figure(figsize=(10,5))
plt.title('The Filtered Signal')
plt.plot(t, y)
plt.grid(True)
plt.show()

# %%

# Re-run the frequency analysis plot on the clean (filtered) signal
fs = 1e6
freq_analysis_plot2(y, t, fs, True, [0, 1.8e3], [2e3, 200e3], [1.7e3, 2.1e3], (7,10), 'The Filtered Signal Characteristics', ['Low Frequency Noise', 'High Frequency Noise', 'Desired Signal Band'], ['Magnitude', 'Phase'])

