from scipy.signal import butter, filtfilt, freqz;

class Butterworth:
	filter_mode = "";
	sample_rate = 0.0;
	cutoff_freq = 0.0;
	filter_order = 1;
	lowcut = 0.0
	highcut = 0.0
	
	def __init__(self, mode, fs, cutoff, order, lowcut = 0.0, highcut = 0.0):
		self.filter_mode = mode;
		self.sample_rate = fs;
		self.cutoff_freq = cutoff;
		self.filter_order = order;
		
		if (lowcut != 0.0 and highcut != 0.0):
			self.lowcut = lowcut
			self.highcut = highcut
		
	def getCoefs(self):
		nyq = 0.5 * self.sample_rate;
		
		if (self.lowcut != 0.0 and self.highcut != 0.0):
			b, a = butter(self.filter_order, [self.lowcut / nyq, self.highcut / nyq], btype=self.filter_mode, analog=False)
		else:
			b, a = butter(self.filter_order, self.cutoff_freq / nyq, btype=self.filter_mode, analog=False)
		
		return b, a

	def filter(self, data):
		b, a = self.getCoefs()
		y = filtfilt(b, a, data)
		return y
