import location
import gobject
 
def on_error(control, error, data):
    print "location error: %d... quitting" % error
    data.quit()
 
def on_changed(device, data):
    if not device:
        return
    if device.fix:
        if device.fix[1] & location.GPS_DEVICE_LATLONG_SET:
            print "lat = %f, long = %f" % device.fix[4:6]
            # data.stop() commented out to allow continuous loop for a reliable fix - press ctrl c to break the loop, or program your own way of exiting)
        if device.fix[1] & location.GPS_DEVICE_ALTITUDE_SET:
            print "alt = %f" % device.fix[7]
        print "horizontal accuracy: %f meters" % (device.fix[6] / 100)
    # FIXME: not supported yet in Python
    #if device.cell_info:
    #    if device.cell_info[0] & location.GSM_CELL_INFO_SET:
    #        print "Mobile Country Code GSM: %d" % device.cell_info[1][0]
    #    if device.cell_info[0] & location.WCDMA_CELL_INFO_SET:
    #        print "Mobile Country Code WCDMA: %d" % device.cell_info[2][0]
 
        print "Satellites in view: %d, in use: %d" % (device.satellites_in_view, device.satellites_in_use)

def on_stop(control, data):
    print "quitting"
    data.quit()
 
def start_location(data):
    data.start()
    return False
 
loop = gobject.MainLoop()
control = location.GPSDControl.get_default()
device = location.GPSDevice()
control.set_properties(preferred_method=location.METHOD_USER_SELECTED,
                       preferred_interval=location.INTERVAL_DEFAULT)
 
control.connect("error-verbose", on_error, loop)
device.connect("changed", on_changed, control)
control.connect("gpsd-stopped", on_stop, loop)
 
gobject.idle_add(start_location, control)
 
loop.run()
