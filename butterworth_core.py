from scipy.signal import butter, lfilter, freqz;

class Butterworth:
	filter_mode = "";
	sample_rate = 0.0;
	cutoff_freq = 0.0;
	filter_order = 1;
	
	def __init__(self, mode, fs, cutoff, order=5):
		self.filter_mode = mode;
		self.sample_rate = fs;
		self.cutoff_freq = cutoff;
		self.filter_order = order;
		
	def getCoefs(self):
		nyq = 0.5 * self.sample_rate;
		normal_cutoff = self.cutoff_freq / nyq;
		print self.filter_order;
		print normal_cutoff
		b, a = butter(self.filter_order, normal_cutoff, btype=self.filter_mode, analog=False)
		return b, a

	def filter(self, data):
		b, a = self.getCoefs()
		y = lfilter(b, a, data)
		return y
