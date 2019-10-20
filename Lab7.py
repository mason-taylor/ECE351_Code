#%%
# Preliminary Setup
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

halfsize_figure = (8,3)
fullsize_figure = (16,3)

#Default figure size is smaller figure
plt.rcParams.update({'font.size': 12, 'figure.figsize': fullsize_figure})

stepsize = 0.1

#%% [markdown]
# # Introduction
# We will be performing block diagram analysis to find the
# transfer functions of systems represented by connected blocks
# with arbitrary transfer functions. Block diagram analysis is 
# important since it enables us to find the transfer functions
# systems with various components when we know the transfer functions
# of all the components. We will perform two types of analysis
# on our simple block diagram, open-loop, and closed-loop,
# and each will yield a different function. The open-loop transfer
# function is the transfer function of the shortest path in from input
# to output in the system. The closed-loop transfer function is the 
# commonly used total transfer function. We will analyze the following
# diagram:
# \begin{figure}[h]
#    \centering
#     \includegraphics[width=0.7\textwidth]{C:\\Users\Mason Taylor\\OneDrive - University of Idaho\\ECE 351\\Lab7\\circuit.png}
#     \caption{The block diagram we will analyze.}
# \end{figure}
# 
# # Equations
# ## Part 1
# The transfer functions of individual components
# are given by the following:
# $$ G(s)=\frac{s+9}{(s-8)(s+2)(s+4)} $$
# $$ A(s)= \frac{s+4}{(s+1)(s+3)} $$
# $$ B(s)= (s+12)(s+14) $$
# It is quite easy to see the poles and zeros of the functions in
# this factored form. For $G(s)$ zeros are -9, poles are 8,-2,-4
# for $A(s)$, zeros are -4, poles are -1, -3, finally for $B(s)$
# the zeros are -12, -14 with no poles. 
# <br><br>The open loop tranfer function will simply follow the top branch
# and therefore it can be written as:
# $$ H_{OL}(s)=A(s)G(s)=\frac{s+9}{(s-8)(s+2)(s+1)(s+3)} $$
# The poles of this function are at 8, -2, -1, -3 which means
# that this response is NOT stable due to the pole at 8. This will cause
# the output to be unbounded, and with a minor input will rapidly go out of
# control. #
# ## Part 2
# We now find the closed loop transfer function, which will be:
# $$ \frac{A(s)G(s)}{1+G(s)B(s)} $$
# To find this function, we will use scipy.signal.convolve
# to multiply out the binomial terms and fully expand the numerator and denominator.
# Symbolically, in terms of numerator and denominator of each function, we can find the 
# representation of the total transfer function:
# $$ \frac{\frac{numA*numG}{denA*denG}}{1+\frac{numG*numB}{denG*denB}} $$ 
# Which simplifies to (noting that denB = 1):
# $$ \frac{numA*numG}{denA*(denG+numG*numB)} $$
# Using the convolve function to do the multiplication, we obtain:
# $$ H(s)=\frac{s^2+13s+36}{2s^5+41s^4+500s^3+2995s^2+6878s+4344} $$
# This function has various real and complex poles, but the real portions
# are all negative, meaning that this function is stable.
# # Results
# ## Part 1 Results 
# Shown first are the poles and zeros of the open loop transfer function
# then, the plot of the open loop transfer function.
#%%
Gs = ([1,9],[1,-2,-40,-64])
As = ([1,4],[1,4,3])
Bs = ([1,26,168], [1])

d = sig.convolve(sig.convolve([1,-8], [1,2]), sig.convolve([1,1], [1,3]))
H_ol = ([1,9], d)

print("Poles and Zeros of the open loop transfer function:")
(z,p,k) = sig.tf2zpk(H_ol[0], H_ol[1])
print('Zeros:', z, 'Poles:', p)

t = np.arange(0, 5 + stepsize, stepsize)

(Tr,y2) = sig.step(H_ol)


plt.figure(figsize=fullsize_figure)

plt.subplots_adjust(top=2,bottom=0)

plt.subplot(1,1,1)
plt.plot(Tr,y2)
plt.grid(True)
plt.ylabel('h_ol(t)*u(t)')
plt.title('Open Loop step response')

#%% [markdown]
# ## Part 2 Results
# We now find the closed loop step response of the given system. To do this, 
# we will use the library function __scipy.signal.convolve__ to perform the 
# multinomial multiplication for us, and give the coefficients of each s term
# in the form needed for the residue function.

#%%

num = sig.convolve(As[0], Gs[0])
den = sig.convolve(As[1], (Gs[1] + sig.convolve(Gs[0], Bs[0])))

H_cl = (num, den)

print('Poles and Zeros of the closed loop (overall) tranfer function:')
print('Zeros: ', np.roots(num))
print('Poles: ', np.roots(den))

t = np.arange(0, 4 + stepsize, stepsize)

(Tr,y2) = sig.step(H_cl)


plt.figure(figsize=fullsize_figure)

plt.subplots_adjust(top=2,bottom=0)

plt.subplot(1,1,1)
plt.plot(Tr,y2)
plt.grid(True)
plt.ylabel('h(t)*u(T)')
plt.title('Closed Loop step response')

#%% [markdown]
# # Questions
# 1. __In Part 1, why does convolving the factored terms using `scipy.signal.convolve()`
# result in the expanded form of the numerator and denominator? Would this work with your
# user-defined convolution function from Lab 3? Why or why not?__<br><br>
# This is because convolve scales 1 function by each value of the other function
# and sums the results, keeping them aligned based on the shift of the second function.
# This process results in a process similiar to FOIL but scaled to any multinomial.
# The process would work equally well with the custom convolve function as long as the 
# time step is given as 1. <br><br>
# 2. __Discuss the difference between the open- and closed-loop systems from Part 1 and Part 2.
# How does stability differ for each case, and why?__<br><br>
# The open loop transfer function does not account for the feedback in the system nad simply
# takes the most direct path from input to output. Consequently, it can result in a response
# that is much more volatile since it is not regulated by the negative feedback 
# loop. However, the closed loop transfer function considers the full effect of 
# all the components, and thus turns out to be stable system due to the negative feedback.<br><br>
# 3. __What is the difference between `scipy.signal.residue()` used in Lab 6 and
# `scipy.signal.tf2zpk()` used in this lab?__<br><br>
# Residue performs a partial fraction expansion into linear terms whereas
# tf2zpk is more like factoring the numerator and denominator of the function and
# examining to find the poles and zeros of the function. <br><br>
# 4. __Is it possible for an open-loop system to be stable? What about for a closed-loop system to
# be unstable? Explain how or how not for each.__<br><br>
# It is quite possible for both of the situations to occur. If the transfer function of each component in the 
# open-loop path has only negative poles, then the open-loop function will be stable.
# If the closed-loop system contains a positive feedback loop, it is very likely it will be unstable.
# # Conclusion
# In this lab we have examined block diagrams and transfer functions by manual analysis
# and using functions availabe in Python libraries. We have looked at stability and instability and how
# to determine whether a given system is stable or not depending on the poles
# and zeros of the transfer function. Functions with poles in the positive quandrant will be
# unstable and if all the poles are negative, it will be stable. 


#%%
