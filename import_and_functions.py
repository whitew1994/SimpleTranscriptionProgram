# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 13:42:46 2016

@author: Owner
"""

from __future__ import division
from numpy import fft
from numpy.fft import rfft, irfft, fftfreq
from scipy.io import wavfile # Importing the required package for importing wav files into python
from scipy import signal
from scipy import *
from scipy.signal import blackmanharris
import wave
import math
import time
import matplotlib.image as mpimg


def convert(f_i):     # Function to convert frequency values to their equivient piano key
    n = 12*log2(f_i/440) + 49
    n = around(n)
    return n.astype(int)
    
def unvert(n):        # Opposite of the above function  
    f = 2**((n-49)/12)*440
    return f

def hpfilter(freq, numSamples):    # Creates a highpass filter to be applied to data    
    b, a = signal.butter(2, (freq*2*pi), 'highpass', analog=True)
    c, d = signal.freqs(b, a, linspace(0,4091.904,numSamples))
    e = abs(d)
    return e
    
def fourier(b,N,dt): # Performs a fast fourier transform and returns the new axe's
    fs = (1./float(dt)) # The maximum frequency
    window = blackman(N) # create a blackman envelope
    windowed_data = window*b
    freq_domain = fft.fft(windowed_data,N)
    freq = fft.fftfreq(N,dt)
    return freq, freq_domain
    
def freq_from_HPS(sig,fs,cutoff,maxharms):
    """
    Estimate frequency using harmonic product spectrum (HPS)
    
    """
    windowed = sig * blackmanharris(len(sig))  # Applying a blackman harris window before fft
    
    c = abs(rfft(windowed))
    c = c*hpfilter(cutoff,len(c))
    downsamples= []
    H_sum = ones(len(c))
    
    for x in range(1,maxharms): # Downsamples the data by averaging aound the pont in question
        tot_harm = 0            # Done as many times as there are harmonics
        for i in range(x):
            tot_harm += c[i::x][:len(c)/x]
        downsamples.append(tot_harm/x)
        
    for i in range(len(downsamples)):      # Calculating the HPS to be returned
        H_sum = H_sum[:len(downsamples[i])]
        H_sum *= downsamples[i]
        
    return H_sum 