from scipy import signal

def filtering(fil, data, nyq=None, cut_low=None, cut_high=None, numtaps=225):
    """FIR Filtering

     Parameters
    ----------------------------------
    data: signal data
    nyq: nyquist frequency
    fil: h (high pass), l (low pass), b (band pass)
         bs (band stop), m (median)
    cut_high: cutting frequency (high pass)
    cut_low: cutting frequency (low pass)
    numstap: tap number
    """

    if fil is "h":  # high pass
        b = signal.firwin(numtaps, cut_high, pass_zero=False, nyq=nyq)
    elif fil is "l":  # low pass
        b = signal.firwin(numtaps, cut_low, nyq=nyq)
    elif fil is "b":  # band pass
        b = signal.firwin(numtaps, [cut_low, cut_high], pass_zero=False, nyq=nyq)
    elif fil is "bs":  # band stop
        b = signal.firwin(numtaps, [cut_low, cut_high], nyq=nyq)
    elif fil is "m":  # median filter
        return signal.medfilt(data, numtaps)
    return signal.lfilter(b, 1, data)
