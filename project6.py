# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
from IPython.display import HTML

halfsize_figure = (8,3)
fullsize_figure = (16,3)

#Default figure size is smaller figure
plt.rcParams.update({'font.size': 12, 'figure.figsize': fullsize_figure})

stepsize = 0.005


def r(t):
    if t > 0:
        return t
    return 0

def u(t):
    if t >= 0:
        return 1
    return 0


#Part 1 - Step response plots

def h(t):
    y = np.zeros((len(t),1))
    for i in range(len(t)):
        y[i] = (1/2 + np.exp(-6*t[i]) - (1/2)*np.exp(-4*t[i]))*u(t[i])
    return y

H = ([1,6,12], [1,10,24])



t = np.arange(0, 2 + stepsize, stepsize)

y1 = h(t)

(Tr,y2) = sig.step(H, T=t)


#plt.figure(figsize=fullsize_figure)

plt.subplots_adjust(top=2,bottom=0)

plt.subplot(2,1,1)
plt.plot(t,y1)
plt.grid(True)
plt.ylabel('h(t)')
plt.title('Step response of system')

plt.subplot(2,1,2)
plt.plot(t,y2)
plt.grid(True)
plt.ylabel('sig.step')
#plt.title('')



plt.show()


H = ([1,6,12], [1,10,24,0])

#partial fraction expansion of H
(r,p,k) = sig.residue(H[0], H[1])

for i in range(len(r)):
    print('\n','\nr[',i,']=',r[i],'\np[',i,']=',p[i],'\n')


#Part 2
t = np.arange(0, 4.5 + stepsize, stepsize)

d = [1,18,218,2036,9085,25250]
n = [25250]


(Tr,y2) = sig.step((n,d), T=t)




#plt.figure(figsize=fullsize_figure)

plt.subplots_adjust(top=2,bottom=0)
plt.title('Step response of system 2')
plt.subplot(1,1,1)
plt.plot(t,y2)
plt.grid(True)
plt.ylabel('sig.step (2)')
plt.show()
#plt.title('')

    
def cosine_method(r,p,t):
    y = np.zeros((len(t),1))
    for j in range(len(t)):
        for i in range(len(r)):
            y[j] += (abs(r[i])*np.exp(np.real(p[i])*t[j])
            *np.cos(np.imag(p[i])*t[j]+np.angle(r[i])))
    return y

d = [1,18,218,2036,9085,25250,0]

(r,p,k) = sig.residue(n,d)


for i in range(len(r)):
    print('\n','\nr[',i,']=',r[i],'\np[',i,']=',p[i],'\n')

y3 = cosine_method(r,p,t)
#print (y3)

#plt.figure(figsize=fullsize_figure)

plt.subplots_adjust(top=2,bottom=0)
plt.title('Step response of system 2, using custom cosine method')
plt.subplot(1,1,1)
plt.plot(t,y3)
plt.grid(True)
plt.ylabel('sig.step (3)')

plt.show()
    


