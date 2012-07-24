#!/usr/bin/env python
#
# Adapted by Daniel Belasco Rogers (danbelasco@yahoo.co.uk)
# from the following script:
# Copyright (c) IBM Corporation, 2006. All Rights Reserved.
# Author: Simon Johnston (skjohn@us.ibm.com)

import serial
import datetime
import sys

# Usual location (address) of gps plugged into usb (linux)
GPSADDR = "/dev/ttyUSB0"
# Baud rate of device - 115200 for dataloggers, 4800 for Garmin etrex
BAUD = 115200


class GPSDevice(object):
    """ General GPS Device interface for connecting to serial port GPS devices
        using the default communication params specified by the National Marine
        Electronics Association (NMEA) specifications.
    """

    def __init__(self, commport):
        """ GPSDevice(port)
            Connects to the serial port specified, as the port numbers are
            zero-based on windows the actual device string would be "COM" +
            port+1.
        """
        self.commport = commport
        self.port = None

    def open(self):
        """ open() open the GPS device port, the NMEA default serial
            I/O parameters are defined as 115200,8,N,1. (4800 for
            garmin)
        """
        nmea_params = {
            'port': self.commport,
            'baudrate': BAUD,
            'bytesize': serial.EIGHTBITS,
            'parity': serial.PARITY_NONE,
            'stopbits': serial.STOPBITS_ONE
        }
        if self.port:
            print 'Device port is already open'
            sys.exit(2)
        try:
            self.port = serial.Serial(**nmea_params)
            self.port.open()
        except serial.SerialException:
            print """
Problem connecting to GPS
Is device connected and in NMEA transfer mode?
"""
            sys.exit(2)

    def read(self):
        """ read() -> dict read a single NMEA sentence from the device
        returning the data as a dictionary. The 'sentence' key will
        identify the sentence type itself with other parameters
        extracted and nicely formatted where possible.
        """
        sentence = 'error'
        line = self._read_raw()
        if line:
            record = self._validate(line)
            if record:
                if record[0] in _decode_func:
                    return _decode_func[record[0]](record)
                else:
                    sentence = record[0]
        return {
            'sentence': sentence
        }

    def read_all(self):
        """ read_all() -> dict A generator allowing the user to read
        data from the device in a for loop rather than having to craft
        their own looping method.
        """
        while 1:
            try:
                record = self.read()
            except IOError:
                raise StopIteration
            yield record

    def close(self):
        """ close() Close the port, note you can no longer read from
            the device until you re-open it.
        """
        if not self.port:
            print 'Device port not open, cannot close'
            sys.exit()
        self.port.close()
        self.port = None

    def _read_raw(self):
        """ _read_raw() -> str Internal method which reads a line from
            the device (line ends in \r\n).
        """
        if not self.port:
            print 'Device port not open, cannot read'
            sys.exit()
        return self.port.readline()

    def _checksum(self, data):
        """ _checksum(data) -> str Internal method which calculates
        the XOR checksum over the sentence (as a string, not including
        the leading '$' or the final 3 characters, the ',' and
        checksum itself).
        """
        checksum = 0
        for character in data:
            checksum = checksum ^ ord(character)
        hex_checksum = "%02x" % checksum
        return hex_checksum.upper()

    def _validate(self, sentence):
        """ _validate(sentence) -> str
            Internal method.
        """
        sentence.strip()
        if sentence.endswith('\r\n'):
            sentence = sentence[:len(sentence)-2]
        if not sentence.startswith('$GP'):
            # Note that sentences that start with '$P' are proprietary
            # formats and are described as $P<mid><sid> where MID is the
            # manufacturer identified (Magellan is MGN etc.) and then the
            # SID is the manufacturers sentence identifier.
            return None
        star = sentence.rfind('*')
        if star >= 0:
            check = sentence[star + 1:]
            sentence = sentence[1:star]
            sum = self._checksum(sentence)
            if sum <> check:
                return None
        sentence = sentence[2:]
        return sentence.split(',')


# The internal decoder functions start here.

def format_date(datestr):
    """ format_date(datestr) -> str
        Internal function. Turn GPS DDMMYY into DD/MM/YY
    """
    if datestr == '':
        return ''
    year = int(datestr[4:])
    now = datetime.date.today()
    if year + 2000 > now.year:
        year = year + 1900
    else:
        year = year + 2000
    the_date = datetime.date(year, int(datestr[2:4]), int(datestr[:2]))
    return the_date.isoformat()


def format_time(timestr):
    """ format_time(timestr) -> str Internal function. Turn GPS HHMMSS
        into HH:MM:SS UTC
    """
    if timestr == '':
        return ''
    utc_str = ' +00:00'
    the_time = datetime.time(int(timestr[:2]),
                             int(timestr[2:4]),
                             int(timestr[4:6]))
    return the_time.strftime('%H:%M:%S') #+ utc_str


def format_latlong(data, direction):
    """ formatp_latlong(data, direction) -> str

        Internal function. Turn GPS HHMM.nnnn into standard HH.ddddd

    """
    # Check to see if it's HMM.nnnn or HHMM.nnnn or HHHMM.nnnn
    if data == '':
        return 0 # this to stop blowing up on empty string (Garmin etrex)
    dot = data.find('.')
    if (dot > 5) or (dot < 3):
        raise ValueError, 'Incorrect formatting of "%s"' % data
    hours = data[0:dot-2]
    mins = float(data[dot-2:])
    if hours[0] == '0':
        hours = hours[1:]
    if direction in ['S', 'W']:
        hours = '-' + hours
    decimal = mins / 60.0 * 100.0
    decimal = decimal * 10000.0
    return '%s.%06d' % (hours, decimal)


def _convert(v, f, d):
    """ a multi-purpose function that converts
        into a number of data types
        v = value
        f = data type e.g int, float string
        d = default value if it doesn't work
    """
    try:
        return f(v)
    except:
        return d


def _decode_gsv(data):
    """ decode_gsv(date) -> dict
        Internal function.
        data[0] = sentence
        data[1] = number of sentences
        data[2] = sentence number
        data[3] = satellites in view
    """
    if data[3] == '00':
        print """
GPS not receiving enough satellites or outputting strange values
Try turning GPS off and back on again before re-starting script
"""
        sys.exit(2)
    sats = []
    if data[2] < data[1]: # if this isn't the last sentence
        blockno = 4       # the number of blocks in a full sentence
    elif data[2] == data[1]: # this IS the last sentence
        # get the remaining number of blocks:
        blockno = _convert(data[3], int, 0) % 4
        if blockno == 0:
            blockno = 4
        #print 'number of satellites: %s' % data[3]
        #print 'number of sentences: %s' % data[1]
        #print 'number of satellites in last sentence: %s' % blockno
    for i in range(blockno * 4): # iterate through the sentence
        sats.append(_convert(data[i + 4], int, 0))
    return {
        'sentence': data[0],
        'Sentence_no.': _convert(data[2], int, 0),
        'NumberOfSentences': _convert(data[1], int, 0),
        'inview': _convert(data[3], int, 0),
        'satellite_data_list': sats
    }


def _decode_rmc(data):
    """ Simply parses the rmc sentence into a dictionary that makes it
    easier to query for values
    """
    return {
        'sentence': data[0],
        'time': format_time(data[1]),
        'active': data[2],
        'latitude': _convert(('%s' % format_latlong(data[3], data[4])),
                             float, 0),
        'longitude': _convert(('%s' % format_latlong(data[5], data[6])),
                              float, 0),
        'knots': _convert(data[7], float, 0),
        'bearing': _convert(data[8], float, 0),
        'date': format_date(data[9]),
        'mag_var': '%s,%s' % (data[10], data[11])
    }

# dictionary that maps the sentences onto functions
_decode_func = {
    'GSV': _decode_gsv,
    'RMC': _decode_rmc
}


def main():
    """
    test the script by printing the outputs
    """
    # setup and connect to gps
    gps = GPSDevice(GPSADDR)
    gps.open()
    for record in gps.read_all():
        print record


# test function
if __name__ == '__main__':
    sys.exit(main())
