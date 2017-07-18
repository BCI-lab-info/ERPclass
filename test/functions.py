from scipy import signal

class Filtering(object):
    """FIR Filtering

     Parameters
    ----------------------------------
    fs: frequency
    fil: h (high pass), l (low pass), b (band pass)
         bs (band stop), m (median)
    cut_high: cutting frequency (high pass)
    cut_low: cutting frequency (low pass)
    numstap: tap number
    sampling_rate (over 1): If 1, no resampling. else downsampling
    ignore: index for ignoring first few signal
            if None, no ignoring

     Attribute
    ----------------------------------
    nyq: nyquist frequency
    """


    def __init__(self, fs, numtaps=225, cut_low=None, cut_high=None,
                 sampling_rate=1, ignore=None):
        self.fs = fs
        self.nyq = fs/2
        self.numtaps = numtaps
        self.cut_low = cut_low
        self.cut_high = cut_high
        self.sampling_rate = sampling_rate
        self.ignore = ignore

    def filtering(self, fil, data):
        """FIR Filtering

        (1) FIR Filtering
        (2) Downsampling by 'sampling_rate'

         Parameters
        ----------------------------------
        data: signal data, ndarray (sample,)
        fil: h (high pass), l (low pass), b (band pass)
             bs (band stop), m (median)

         Return
        ----------------------------------
        Filtered signal
        """

        # Filtering
        if fil is "m":  # median filter
            data = signal.medfilt(data, self.numtaps)
        else:
            if fil is "h":  # high pass
                b = signal.firwin(self.numtaps, self.cut_high,
                                  pass_zero=False, nyq=self.nyq)
            elif fil is "l":  # low pass
                b = signal.firwin(self.numtaps, self.cut_low, nyq=self.nyq)
            elif fil is "b":  # band pass
                b = signal.firwin(self.numtaps, [self.cut_low, self.cut_high],
                                  pass_zero=False, nyq=self.nyq)
            elif fil is "bs":  # band stop
                b = signal.firwin(self.numtaps, [self.cut_low, self.cut_high], nyq=self.nyq)
            data = signal.lfilter(b, 1, data)

        # Ignoring first step
        if self.ignore is not None:
            data = data[self.ignore:-1]

        # Resampling (down sampling)
        data = data[[i for i in range(0, len(data), self.sampling_rate)]]
        return data
