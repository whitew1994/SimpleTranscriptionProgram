# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 13:37:31 2016

@author: Owner
"""
import pyaudio
import wave

def Record(time,name):
    chunk_size = 1024  # deciding how frequently to take a data reading
    Format = pyaudio.paInt16
    Channels = 2
    Rate = 44100 # The samping rate
    output_name = name

    p = pyaudio.PyAudio()

    stream = p.open(format=Format,channels=Channels,rate=Rate,input=True,frames_per_buffer=chunk_size) # Open a stream to th mic

    print "recording"

    frames = []

    for i in range(0, int(Rate/chunk_size*time)): Collect data at the desired rate
        dat = stream.read(chunk_size)
        frames.append(dat)
    
    print "done recording"

    stream.stop_stream()
    stream.close()
    p.terminate()

    f = wave.open(output_name,'wb') # Saving the output file
    f.setnchannels(Channels)
    f.setsampwidth(p.get_sample_size(Format))
    f.setframerate(Rate)
    f.writeframes(b''.join(frames))
    f.close()