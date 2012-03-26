#from Numeric import *
#from MLab import *
#from FFT import *
#from dislin import *
import numpy
from numpy import zeros
from array import array
import wave
import sys
import struct


filename = "testData/horse.wav"
windowSize = 16

# open the wave file
fp = wave.open(filename,"rb")

sample_rate = fp.getframerate()
total_num_samps = fp.getnframes()
fft_length = int(windowSize)
num_fft = (total_num_samps / fft_length ) - 2
print num_fft

# create temporary working array
temp = zeros((num_fft,fft_length),float)

# read in the data from the file
for i in range(num_fft):
    tempb = fp.readframes(fft_length)
    
    print ">", tempb, "<", len(tempb)
    print ">", "<"
    temp[i,:] = numpy.array(array("h",tempb)) - 128.0
fp.close()

# Window the data
#temp = temp * hamming(fft_length)

# Transform with the FFT, Return Power
freq_pwr  = 10*log10(1e-20+abs(real_fft(temp,fft_length)))

n_out_pts = (fft_length / 2) + 1

# Plot the result
y_axis = 0.5*float(sample_rate) / n_out_pts * arange(n_out_pts)
x_axis = (total_num_samps / float(sample_rate)) / num_fft * arange(num_fft)
setvar('X',"Time (sec)")
setvar('Y',"Frequency (Hertz)")
conshade(freq_pwr,x_axis,y_axis)
disfin()
