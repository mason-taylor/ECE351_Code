#%%
# Preliminary Setup
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import control as con

fullsize_figure = (16,8)

stepsize = 100

R = 1000
L = 27e-3
C = 100e-9

w = np.arange(1e3, 1e6 + stepsize, stepsize)
hmag = (w/(R*C)) / ( np.sqrt((1/(L*C) - w**2)**2 + (w/(R*C))**2) )  
hphase = (np.pi/2 - np.arctan( (w/(R*C)) / ((1/(L*C) - w**2)) ))

#Adjust the phase
for i in range(len(w)):
    if ( (1/(L*C) - w[i]**2) < 0):
        hphase[i] -= np.pi

#Using the hand derived transfer function
plt.figure(figsize=fullsize_figure)
plt.subplot(2,1,1)
plt.title('Magnitude of H (Hand Derived)')
plt.semilogx(w, 20*np.log10(hmag))
plt.grid(True)

plt.subplot(2,1,2)
plt.title('Phase of H')
plt.semilogx(w, 180*hphase/np.pi)
plt.grid(True)
plt.show()

#Using the signal.bode method
numh = [1/(R*C), 0]
denh = [1, 1/(R*C), 1/(L*C)]

[freq, mag, phase] = sig.bode((numh,denh))

plt.figure(figsize=fullsize_figure)
plt.subplot(2,1,1)
plt.title('Magnitude of H (Signal.Bode)')
plt.semilogx(freq, mag)
plt.grid(True)

plt.subplot(2,1,2)
plt.title('Phase of H')
plt.semilogx(freq, phase)
plt.grid(True)
plt.show()

#Using control.TransferFunction to derive the transfer function of the system
#based on the s domain numerator and denominator
sys = con.TransferFunction(numh, denh)

_ = con.bode( sys , w , dB = True , Hz = True , deg = True , Plot = True )

#%%

fs = 1e6
stepsize = 1/fs
t = np.arange(0, .01 + stepsize, stepsize)

#This is our input function
func = np.cos(2*np.pi * 100*t) + np.cos(2*np.pi*3024*t) + np.sin(2*np.pi*50000*t)

plt.subplot(1,1,1)
plt.title('Plot of Input Function')
plt.plot(t, func)
plt.ylabel('x(t)')
plt.grid(True)
plt.show()

fs = 1e6
#Now we can get the results of running the input function through the 
# transfer function
(num,den) = sig.bilinear(numh,denh,fs)
y = sig.lfilter( num,den, func)



plt.subplot(1,1,1)
plt.title('Plot of Output Function')
plt.plot(t, y)
plt.ylabel('y(t)')
plt.grid(True)
plt.show()

# %%
