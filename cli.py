#!/usr/bin/env python
# - *- coding: utf- 8 - *-

exec(open("./butterworth_core.py").read())

import numpy as np;
import matplotlib.pyplot as plt;

class ButterworthCli:
	ftype = ""
	t = 0.0
	fs = 0.0
	cutoff = 0.0
	order = 0
	lowcut = 0.0
	highcut = 0.0
	data = []
	x = []
	
	butterw = 0
	
	def __init__(self):
		print ("### Butterworth filter CLI tool ###")

		self.ftype = input("1. Enter Butterworth filter type (lowpass, highpass, bandpass):")
		self.t = float(input("2. Enter sample rate in seconds (example: 0.0001):"))
		self.fs = 1 / (2 * self.t)
		print ("Sampling freq: ", self.fs)
		self.processUserSignal()
		
		if (self.ftype == "lowpass"):
			self.lowpass_getParams()
		elif (self.ftype == "highpass"):
			self.highpass_getParams()
		elif (self.ftype == "bandpass"):
			self.bandpass_getParams()
		else:
			print ("Wrong filter type!");
			exit(0)
		
		self.filter()
		
			
	def lowpass_getParams(self):	
		self.cutoff = float(input("5. Enter cutoff frequency (example: 500):"))
		self.order = int(input("6. Enter desired filter order (example: 6):"))
		
		self.butterw = Butterworth(self.ftype, self.fs, self.cutoff, self.order);
		b, a = self.butterw.getCoefs()
		
		w, h = freqz(b, a)
		plt.plot((0.5 * self.fs * w) / np.pi, abs(h))
		plt.xlabel('Frequency (Hz)')
		plt.ylabel('Gain')
		plt.grid(True)
		plt.show()
		
	def highpass_getParams(self):	
		self.cutoff = float(input("5. Enter cutoff frequency (example: 1250.0):"))
		self.order = int(input("6. Enter desired filter order (example: 6):"))
		
		self.butterw = Butterworth(self.ftype, self.fs, self.cutoff, self.order);
		b, a = self.butterw.getCoefs()
		
		w, h = freqz(b, a)
		plt.plot((0.5 * self.fs * w) / np.pi, abs(h))
		plt.xlabel('Frequency (Hz)')
		plt.ylabel('Gain')
		plt.grid(True)
		plt.show()
		
	def bandpass_getParams(self):
		self.lowcut = float(input("5. Enter low cutoff frequency (example: 500.0):"))
		self.highcut = float(input("6. Enter high cutoff frequency (example: 1250.0):"))
		self.order = int(input("7. Enter desired filter order (example: 6):"))
		
		self.butterw = Butterworth("band", self.fs, self.cutoff, self.order, self.lowcut, self.highcut);
		b, a = self.butterw.getCoefs()
		
		w, h = freqz(b, a)
		plt.plot(0.5 * self.fs * w / np.pi, abs(h))
		plt.xlabel('Frequency (Hz)')
		plt.ylabel('Gain')
		plt.grid(True)
		plt.show()
		
	def processUserSignal(self):
		T = float(input("3. Enter length of signal in seconds (example: 0.02):"))
		#T = 0.02
		n = int(T * self.fs)
		self.x = np.linspace(0, T, n, endpoint=False)
		
		user_data = 0
		
		print("4. Noisy signal definition loop:")
		
		while 1:
			Amp = float(input("4.1. Enter amplitude of sinewave (example: 0.1):"))
			Freq = float(input("4.2. Enter frequency of sinewave (example: 1.2):"))
			Phase = float(input("4.3. Enter phase of sinewave (example: 0.1):"))
			
			sinewave = Amp * np.sin(2 * np.pi * Freq * self.x + Phase)
			user_data += sinewave
			
			choice = input("4.4. Continiue? (y/n):")
			if choice == "n":
				break
				
		self.data = user_data
		
		
	def filter(self):
		#x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
		#x += 0.01 * np.sin(2 * np.pi * 312 * t + 0.1)
		#x += 0.02 * np.sin(2 * np.pi * 600 * t + .11)
		#x += 0.03 * np.sin(2 * np.pi * 2000 * t)
		
		y = self.butterw.filter(self.data)

		plt.plot(self.x, self.data, 'b-', label='data')
		plt.plot(self.x, y, 'g-', linewidth=2, label='filtered data')
		plt.xlabel('Time [sec]')
		plt.grid()
		plt.legend()
		plt.show()
		
		
a = ButterworthCli()
