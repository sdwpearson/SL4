# Code for the bonus activity, which automatically does the 
# frequency analysis using only the scope.
# Date: December 21, 2021
# Author: Jianan Zhao and Stewart Pearson

import pyvisa as visa
import time
rm = visa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')
print(rm)
print(rm.list_resources('TCPIP0::?*'))

try:

    print('Opening resources.')

    '''Connect to the instruments'''
    scope = rm.open_resource('TCPIP0::192.168.0.253::hislip0::INSTR')

    print('Opened resources')

    ''' Set up the power supply IO configuration'''
    scope.timeout = 10000  # 10s


    # Define string terminations
    scope.write_termination = '\n'
    scope.read_termination = '\n'

    # Set string terminations
    print('\nVISA termination string (write) set to newline: ASCII ',
          ord(scope.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(scope.read_termination))


    # Get the ID info of the function generator
    print('scope ID string:\n  ', scope.query('*IDN?'), flush=True)

    
    # Set probe attenuation factor to unity. This sometimes gets set to 10 by the 
    # factory reset
    scope.write('CHANnel1:PROBe +1.0')
    scope.write('CHANnel2:PROBe +1.0')

    ''' Setup Freq Analysis '''
    scope.write('FRANalysis:ENABle 1')
    print(scope.query('FRANalysis:ENABle?'))
    scope.write('FRANalysis:FREQuency:MODE SWEep')
    print(scope.query('FRANalysis:FREQuency:MODE?'))
    scope.write('FRANalysis:FREQuency:STARt +20.0E0Hz')
    print(scope.query('FRANalysis:FREQuency:STARt?'))
    scope.write('FRANalysis:FREQuency:STOP +10.0E0kHz')
    print(scope.query('FRANalysis:FREQuency:STOP?'))
    scope.write('FRANalysis:SOURce:INPut CHANnel1')
    print(scope.query('FRANalysis:SOURce:INPut?'))
    scope.write('FRANalysis:SOURce:OUTPut CHANnel2')
    print(scope.query('FRANalysis:SOURce:OUTPut?'))
    scope.write('FRANalysis:SWEep:POINts +100')
    print(scope.query('FRANalysis:SWEep:POINts?'))
    scope.write('FRANalysis:TRACe ALL')
    print(scope.query('FRANalysis:TRACe?'))
    scope.write('FRANalysis:WGEN:VOLTage +5E-03')
    print(scope.query('FRANalysis:WGEN:VOLTage?'))
    scope.write('FRANalysis:RUN')

            
except(KeyboardInterrupt):
    print('Keyboard Interrupted execution!')

except:
    print('Timeout!')

time.sleep(3)
scope.close()
