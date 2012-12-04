import  glob
import  os
import  re

#lsusb to find vendorID and productID:
#Bus 002 Device 005: ID 067b:2303 Prolific Technology, Inc. PL2303 Serial Port
# then call print find_usb_tty("067b","2303")
def find_usb_tty(vendor_id = None, product_id = None) :
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
