#!/usr/bin/env python
# - *- coding: utf- 8 - *-

execfile("./butterworth_core.py");

import numpy as np;
import matplotlib.pyplot as plt;
import Tkinter as tk;

class ButterworthGui:
	data = 0;
	window = 0;
	filter_type = 'low';
	fs = 0;
	cutoff = 0;
	order = 0;
	
	frame1 = 0;
	label1 = 0;
	option1 = 0;
	label2 = 0;
	entry1 = 0;
	label3 = 0;
	label4 = 0;
	label5 = 0;
	label6 = 0;
	entry2 = 0;
	label7 = 0;
	entry3 = 0;
	label8 = 0;
	entry4 = 0;
	b1 = 0;
	b2 = 0;
	
	def __init__(self):
		self.window = tk.Tk();
		self.window.title("Butterworth Filter GUI");
		self.window.geometry("400x400");
		self.initWidgets();
		self.packGui();
		
	def initWidgets(self):
		self.filter_type = tk.StringVar(self.window);
		self.frame1 = tk.Frame(self.window,relief="raised");
		self.label1 = tk.Label(self.window, text="Filter type:", width=20);
		self.option1 = tk.OptionMenu(self.window, self.filter_type, "Low-pass", "High-pass", "Band-pass", command=self.setType);
		self.label2 = tk.Label(self.window, text="Sample rate [1-1000000 mcsec]:", width=30);
		self.entry1 = tk.Entry(self.window, width=20);
		self.entry1.insert(0, "1");
		self.label8 = tk.Label(self.window, text="Filter order:", width=12);
		self.entry4 = tk.Entry(self.window, width=3);
		self.entry4.insert(0, "6");
		
		self.label3 = tk.Label(self.window, text="Noisy signal:", width=20);
		self.label4 = tk.Label(self.window, text="", width=20);
		self.label5 = tk.Label(self.window, text="Add to signal:", width=20);
		self.label6 = tk.Label(self.window, text="Amplitude:", width=3);
		self.entry2 = tk.Entry(self.window, width=3);
		self.entry2.insert(0, "1");
		self.label7 = tk.Label(self.window, text="Frequency:", width=3);
		self.entry3 = tk.Entry(self.window, width=3);
		self.entry3.insert(0, "3");
		self.b1 = tk.Button(self.window, text="Add", command=self.addSinewave);
		self.b2 = tk.Button(self.window, text="Draw graph", command=self.drawGraph);
		
	def packGui(self):
		self.frame1.pack();
		self.label1.pack();
		self.option1.pack();
		self.label2.pack();
		self.entry1.pack();
		self.label8.pack();
		self.entry4.pack();
		
		self.label3.pack();
		self.label4.pack();
		self.label5.pack();
		self.label6.pack();
		self.entry2.pack();
		self.label7.pack();
		self.entry3.pack();

		self.b1.pack()
		self.b2.pack()

		tk.mainloop();
		
	def setType(self, value):
		if (value == "Low-pass"):
			self.filter_type = "low";
		elif (value == "High-pass"):
			self.filter_type = "high";
		else:
			self.filter_type = "pass";
		
		print self.filter_type

	def addSinewave(self):
		fs = 1 / float(self.entry1.get()) * 1000 * 1000;
		
		print "Frequency: "
		print fs
		
		A = float(self.entry2.get());
		fr = float(self.entry3.get());
	
		self.data = self.data + (A * np.sin(2 * np.pi * fr * np.arange(fs) / fs));
		
		print "Data is now:"
		print self.data
		
	def drawGraph(self):	
		fs = 1 / float(self.entry1.get()) * 1000 * 1000; # sample rate in Hz

		self.cutoff = fs * 0.25 # frequency in HZ which we want to drop

		# create class instance and get filter coefs to get frequency response
		butterw = Butterworth(str(self.filter_type), fs, self.cutoff);
		b, a = butterw.getCoefs();

		# draw plot of freq response
		w, h = freqz(b, a, worN=8000)
		plt.subplot(2, 1, 1)
		plt.plot(0.5 * fs * w / np.pi, np.abs(h), 'b')
		plt.plot(self.cutoff, 0.5*np.sqrt(2), 'ko')
		plt.axvline(self.cutoff, color='k')
		plt.xlim(0, 0.5 * fs)
		plt.title("Frequency Response")
		plt.xlabel('Frequency [Hz]')
		plt.grid()

		# filter data
		y = butterw.filter(self.data);

		# draw plot of noisy and filtered data
		plt.subplot(2, 1, 2)
		plt.plot(np.arange(fs), self.data, 'b-', label='data')
		plt.plot(np.arange(fs), y, 'g-', linewidth=3, label='filtered data')
		plt.xlabel('Time [sec]')
		plt.grid()
		plt.legend()

		plt.subplots_adjust(hspace=0.35)
		plt.show()
		

a = ButterworthGui();
