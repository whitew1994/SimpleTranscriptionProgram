# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 14:05:24 2016

@author: Owner
"""
from Record import Record            # Importing constructed functions
from import_and_functions import *
from numpy import fft
from scipy.stats import mode
import time

f = open("Notes.txt","r")      # These two files contain the names of the notes 
notes = str.split(f.read())    # for an full piano keyset, both the names and 
f.close()                      # the lilypond code equivilent
f = open("lilynotes.txt","r")
lilynotes = str.split(f.read())
f.close()

time_r = input("Enter the length of time you wish to record for:\n")
outputname = raw_input("Enter the name of the output file recording (.wav file ending):\n")

Record(time_r,outputname)     # Function that records for an inputted period of time
                              # and saves the file with a .wav file ending  
rate, data = wavfile.read("record.wav") # Importing the saved file

Data = data[:,1]
dt = 1/float(rate)
N = len(Data)
window_size = 1000            # The size of the frame being moved through the data
frame_N = N - window_size     # The maximum number of total frames  
weight_off = 126.             # calculated from backgrund noise, could adapt code to calculate background noise first
weight_on = 300.              # The integral of the magnitude of the window for it
maxharms = 4                  # to be on; The maxium harmonics in the fourier domain
f = zeros(frame_N/100)        # Creatng zeros arrays to be filled in the loop
n = zeros(frame_N/100,dtype=int)
noise_test = zeros(frame_N/100)
snr = zeros(frame_N/100)


count1 = 0                    # Two counts, to count the pauses inbetween notes
count2 = 0                    # And the length of notes themselves 
note_start = []               # Lists for the positions of the start of the notes ets..
note_end = []
note_length = []
pauses = []

for i in range(int(frame_N/100)):  # 100 is how far the window jumps each iteration 
    
    windowed_data = Data[(i*100):(i*100)+window_size]
    
    mag_data = abs(windowed_data)  # Finding the snr of each frame 
    weight = sum(mag_data)/len(mag_data)  
    snr[i] = weight/weight_off        
    
    freq_i = fft.rfftfreq(window_size,dt)  # The frequecy axis for the window
    # maxharms = len(peak.utilis(fft.rfft(windowed_data),thres=0.02,min_spacing = 100)) this is a better way to 
    # find the total number of harmonics although not really sure how peak,utilis works currently 
    HPS_i = freq_from_HPS(windowed_data,rate,50,maxharms)  # Calling the HPS function
    f[i] = freq_i[argmax(HPS_i)]   # Taking the frequency that corresponds to a peak in the HPS
    
    
    if weight > weight_on:  # Calculating binary on/off note data by testing the snr
        noise_test[i] = 1
        n[i] = int(convert(f[i]))-12 # Converting frequency values to their piano key number (also allowing for HPS octave error)        
        count1 = count1 +1
        if noise_test[i-5] == 0 and noise_test[i-1] == 0 and noise_test[i-2] == 0 and noise_test[i-3] == 0 and noise_test[i-4] == 0:
            # Not very neat but I dot know how to truth test all at the same time
            # The multiple truth tests allow for a note flickering on and off 
            note_start.append(i-5)
            pauses.append(count2)
            count2 = 0  
    if noise_test[i] == 0 and noise_test[i-1] == 0 and noise_test[i-2] == 0 and noise_test[i-3] == 0 and noise_test[i-4] == 0 and noise_test[i-5] == 1:
        note_length.append(count1)
        count1 = 0
        note_end.append(i-4)
    if n[i] == 0:
        count2 = count2 + 1
        
pauses = array(pauses)
note_start = array(note_start)
note_end = array(note_end)
note_length = array(note_length)
note_time = note_length*dt*100
note_played = []

# Now can get the console to read out the notes that were played!
# With a sound set the notes could be played back in when they are printed

print "The notes that you just played were:"

for i in range(len(note_start)):
    n_range = n[note_start[i]:note_end[i]]
    note_played.append(mode(n_range)[0][0])
    print notes[note_played[i]-1]
    

print '............ The notes you played will be listed with the timing that they were played ...............'

started = zeros(len(note_length))
start = time.time()
while True:
    j = time.time()
    runtime = j - start-3

    for i in range(len(note_length)):
        if runtime >= (100*dt*note_start[i]):
            if started[i] == 0:
                print notes[int(note_played[i])-1]
                started[i] = 1
                               
    if runtime > time_r:
        break

# Construct a string for using in lily pond, to be plotted

sequence = " "
for i in range(len(note_played)):
    sequence = sequence + lilynotes[note_played[i]-1] + " "

g = open("lilypond.ly","w")
g.write("{\n ")
g.write(sequence)
g.write("\n}")
g.close()


