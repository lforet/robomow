#!/usr/bin/python

import gps, os
import threading
import time
import  glob
import  os
import  re


#sudo apt-get install gpsd gpsd-clients
#gpsd /dev/ttyUSB0 -b -n
#The gpsd server reads NMEA sentences from the gps unit and is accessed on port 2947. You can test if everything is working by running a pre-built gpsd client such as xgps.


def find_usb_tty(vendor_id = None, product_id = None) :
	#lsusb to find vendorID and productID:
	#Bus 002 Device 005: ID 067b:2303 Prolific Technology, Inc. PL2303 Serial Port
	# then call print find_usb_tty("067b","2303")
    tty_devs    = []
    vendor_id = int(vendor_id, 16)
    product_id = int(product_id , 16)
    for dn in glob.glob('/sys/bus/usb/devices/*') :
        try     :
            vid = int(open(os.path.join(dn, "idVendor" )).read().strip(), 16)
            pid = int(open(os.path.join(dn, "idProduct")).read().strip(), 16)
            if  ((vendor_id is None) or (vid == vendor_id)) and ((product_id is None) or (pid == product_id)) :
                dns = glob.glob(os.path.join(dn, os.path.basename(dn) + "*"))
                for sdn in dns :
                    for fn in glob.glob(os.path.join(sdn, "*")) :
                        if  re.search(r"\/ttyUSB[0-9]+$", fn) :
                            #tty_devs.append("/dev" + os.path.basename(fn))
                            tty_devs.append(os.path.join("/dev", os.path.basename(fn)))
                        pass
                    pass
                pass
            pass
        except ( ValueError, TypeError, AttributeError, OSError, IOError ) :
            pass
        pass

    return tty_devs

#print find_usb_tty("067b","2303")



class mobot_gps ( Thread ):

    def __init__( self, command_port, data_port ):
        Thread.__init__( self )
	self.cmd_port = command_port
	self.data_port = data_port

	
    def run(self):
		gps1 = gps.gps(host="localhost", port="2947")
		gps2 = gps.gps(host="localhost", port="2947")
		gps3 = gps.gps(host="localhost", port="2947")
		gps4 = gps.gps(host="localhost", port="2947")
