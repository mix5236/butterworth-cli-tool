#!/usr/bin/env python
# - *- coding: utf- 8 - *-

execfile("./butterworth_core.py")

import numpy as np;
import matplotlib.pyplot as plt;

order = 6 #filter order
fs = 30.0 # sample rate in Hz
cutoff = 3.667 # frequency in HZ which we want to drop

# create class instance and get filter coefs to get frequency response
butterw = Butterworth("low", fs, cutoff, order);
b, a = butterw.getCoefs();

# draw plot of freq response
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5 * fs * w / np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


T = 4.0 # time in seconds
n = int(T * fs) # number of samples
t = np.linspace(0, T, n, endpoint=False)
# make data noisy.
# we want to recover 1.2 Hz signal from this
data = np.sin(1.2 * 2 * np.pi * t) + 1.5 * np.cos(9 * 2 * np.pi * t) + 0.5 * np.sin(12.0 * 2 * np.pi * t)

# filter data
y = butterw.filter(data);

# draw plot of noisy and filtered data
plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=3, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()
