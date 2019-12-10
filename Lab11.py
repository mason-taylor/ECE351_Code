#%%
# Preliminary Setup
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import control as con

fullsize_figure = (10,8)

stepsize = 100

numh = [2,-40]
denh = [1, -10, 16]
fs = 1e6


#
# Copyright (c) 2011 Christopher Felton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The following is derived from the slides presented by
# Alexander Kain for CS506/606 "Special Topics: Speech Signal Processing"
# CSLU / OHSU, Spring Term 2011.
#
#
#
# Modified by Drew Owens in Fall 2018 for use in the University of Idaho's 
# Department of Electrical and Computer Engineering Signals and Systems I Lab
# (ECE 351)
#
# Modified by Morteza Soltani in Spring 2019 for use in the ECE 351 of the U of
# I.
#
# Modified by Phillip Hagen in Fall 2019 for use in the University of Idaho's  
# Department of Electrical and Computer Engineering Signals and Systems I Lab 
# (ECE 351)
# 
# 
# Modified by Mason Taylor in November 2019: Removed explicit color override 
# in plotting unit circle to allow plot to use default color theme so that 
# plots also look right in dark theme applications.
# 
    
def zplane(b,a,filename=None):
    """Plot the complex z-plane given a transfer function.
    """

    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import patches    
    
    # get a figure/plot
    ax = plt.subplot(111)

    # create the unit circle
    uc = patches.Circle((0,0), radius=1, fill=False,
                        ls='dashed')
    ax.add_patch(uc)

    # The coefficients are less than 1, normalize the coeficients
    if np.max(b) > 1:
        kn = np.max(b)
        b = np.array(b)/float(kn)
    else:
        kn = 1

    if np.max(a) > 1:
        kd = np.max(a)
        a = np.array(a)/float(kd)
    else:
        kd = 1
        
    # Get the poles and zeros
    p = np.roots(a)
    z = np.roots(b)
    k = kn/float(kd)
    
    # Plot the zeros and set marker properties    
    t1 = plt.plot(z.real, z.imag, 'o', ms=10,label='Zeros')
    plt.setp( t1, markersize=10.0, markeredgewidth=1.0)

    # Plot the poles and set marker properties
    t2 = plt.plot(p.real, p.imag, 'x', ms=10,label='Poles')
    plt.setp( t2, markersize=12.0, markeredgewidth=3.0)

    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    plt.legend()

    # set the ticks
    #r = 1.5; plt.axis('scaled'); plt.axis([-r, r, -r, r])
    #ticks = [-1, -.5, .5, 1]; plt.xticks(ticks); plt.yticks(ticks)

    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
    
    return z, p, k

# End Copyrighted Code

#%%

(r,p,k) = sig.residuez(numh, denh)

print('H(z)/z =', k[0], end=' ')

for i in range(len(r)):
    print('+','(' + str(r[i]), '/ (z -', str(p[i]) + ')', end=') ')

#%%
_ = zplane(numh, denh)

#%%

(w, h_vals) = sig.freqz(numh, denh, whole=True)

#Using the hand derived transfer function
plt.figure(figsize=fullsize_figure)
plt.subplot(2,1,1)
plt.ylabel('Magnitude')
plt.plot(w/(2*np.pi), np.abs(h_vals))
plt.grid(True)

plt.subplot(2,1,2)
plt.ylabel('Angle (deg)')
plt.plot(w/(2*np.pi), np.angle(h_vals)*180/np.pi)
plt.grid(True)


#%%