#!/usr/bin/env python

import serial
import threading

class MaxSonar(object):
    def __init__(self, port):
        self._ser = self._open_serial_port(port)
        self._should_stop = threading.Event()
        self._start_reading()
    
    def _open_serial_port(self, port):
        ser = serial.Serial(port=port,
                             baudrate=9600,
                             bytesize=serial.EIGHTBITS,
                             parity=serial.PARITY_NONE,
                             stopbits=serial.STOPBITS_ONE,
                             xonxoff=False,
                             rtscts=False,
                             dsrdtr=False,
                             )
        return ser
    
    def _start_reading(self):
        def read():
            while not self._should_stop.isSet():
                data = self._ser.read(5)
                print data
                self._data = int(data[1:3])
        thr = threading.Thread(target=read)
        thr.start()
        return thr
    
    def stop(self):
        self._should_stop.set()
        self._read_thread.wait()
        
    def distances_inches(self):
        return self._data
