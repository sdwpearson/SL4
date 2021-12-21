# Skeleton code for generating a manual Bode Plot
# Using the DSO1202G Oscilloscope and EDU33210 
# Waveform Generator. Comments marked [TODO] need
# to be filled in!
# Date: December 21, 2021
# Author: Jianan Zhao and Stewart Pearson

import numpy
import pyvisa as visa
import matplotlib.pyplot as plt
import time
import math
from GenerateBodePlot import GenerateBodePlot

# Check that the resources are correct
rm = visa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')
print(rm)
print(rm.list_resources('TCPIP0::?*'))

try:

    print('Opening resources.')

    '''Connect to the instruments'''
    scope = rm.open_resource('TCPIP0::192.168.0.253::hislip0::INSTR')
    fxngen = rm.open_resource('TCPIP0::192.168.0.254::5025::SOCKET')

    ''' Set up the power supply IO configuration'''
    scope.timeout = 10000  # 10s
    fxngen.timeout = 10000  # 10s


    # Define string terminations
    scope.write_termination = '\n'
    scope.read_termination = '\n'
    fxngen.write_termination = '\n'
    fxngen.read_termination = '\n'

    # Set string terminations
    print('\nVISA termination string (write) set to newline: ASCII ',
          ord(scope.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(scope.read_termination))
    print('\nVISA termination string (write) set to newline: ASCII ',
          ord(fxngen.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(fxngen.read_termination))


    # Get the ID info of the function generator
    print('scope ID string:\n  ', scope.query('*IDN?'), flush=True)
    print('fxngen ID string:\n  ', fxngen.query('*IDN?'), flush=True)

    ''' Loop through frequencies for Bode plot and measure amplitude '''
    # Choose the number of frequencies and the range based on your expected
    # cut-off frequency of the RC circuit. You'll want to capture the cutoff
    # and a decade or so of the attenuation as well.
    num_freqs = 0 # [TODO] choose the number of frequencies 
    start_freq = 1.1 # [TODO] choose the start frequency exponent (it's in the format 10^start_freq). Don't use the placeholder 1.1
    stop_freq = 1.2 # [TODO] choose the start frequency exponent (it's in the format 10^stop_freq). Don't use the placeholder 1.2
    freqs = numpy.logspace(start=start_freq, stop=stop_freq, num=num_freqs) # get frequencies to try in logarithmic spacing

    ''' [TODO] Set the waveform generator to output a sine wave with amplitude 0.05 and turn on'''
    
    # Set probe attenuation factor to unity. This sometimes gets set to 10 by the 
    # factory reset
    scope.write('CHANnel1:PROBe +1.0')
    scope.write('CHANnel2:PROBe +1.0')

    # Set waveform generator output impdance to high Z
    fxgen.write('OUTPUT:LOAD INF')

    # [TODO] Set vertical scale to +0.05

    # [TODO] Set scope timebase mode to main and reference to center


    ch1_vpp = [0]*num_freqs
    ch2_vpp = [0]*num_freqs
    phase = [0]*num_freqs
    dB = [0]*num_freqs
    freq_idx = 0;
    # [TODO] Complete this for loop through the frequencies to get the 
    # magnitude and phase from the RC circuit
    for freq in freqs: 
        # Make sure the timebase is appropriate for the frequency
        scale_str = 'TIMebase:SCALe '+"{:E}".format(1/freq*2)
        scope.write(scale_str)
        
        # Make sure the scale on the attenuated output signal is appropriate
        if freq_idx != 0:
            scale_str = ':CHANnel2:SCALe '+"{:E}".format(ch2_vpp[freq_idx - 1])
            scope.write(scale_str)  # set vertical scale on attenuated signal

        # [TODO] Set the frequency of the waveform generator to freq

        # [TODO] Set the trigger level to automatic


        ch1_vpp[freq_idx] = 0 # [TODO] measure Vpp in channel 1 here
        ch2_vpp[freq_idx] = 0 # [TODO] measure Vpp in channel 2 here
        phase[freq_idx] = 0 # [TODO] measure phase from channel 2 to channel 1 here
        dB[freq_idx] = 20*math.log10(ch2_vpp[freq_idx]/ch1_vpp[freq_idx]) # dB attenuation
        freq_idx = freq_idx+1
    
    # [TODO] turn off waveform generator

    # Plot the response. Compare with what you know of RC circuits.
    GenerateBodePlot(freqs, dB, phase)
            
except(KeyboardInterrupt):
    print('Keyboard Interrupted execution!')

#except:
    #print('Timeout!')

time.sleep(3)
scope.close()
fxngen.close()
