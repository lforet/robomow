import android,socket,time

droid=android.Android();
ipServer= '192.168.1.180'
portServer= 8095

def sendData():
    # BEGIN
    droid.dialogCreateAlert('Sensor Recorder','Are you ready to record a session?')
    droid.dialogSetPositiveButtonText('Record Now')
    droid.dialogShow()
    response = droid.dialogGetResponse().result
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ipServer, portServer))
    droid.dialogCreateAlert('Record Session','Do you want to record a session?')
    droid.dialogSetPositiveButtonText('Stop')
    droid.dialogSetNegativeButtonText('Restart')
    droid.dialogShow()
    droid.eventClearBuffer()
    droid.startSensingTimed(1,50)
    droid.startLocating()
    #time.sleep(25)
    loc = droid.readLocation()
    #droid.stopLocating()
    #now = str(datetime.datetime.now())

    while True:
        lat = str(loc[1]['gps']['latitude'])
        lon = str(loc[1]['gps']['longitude'])
        event=droid.eventWait().result 
        data=event["data"]
        name=event["name"]
        if name == 'sensors':
            s.send('\n %.3f' % data["time"])
            print data
            for val in ['light', 'accuracy', 'xforce','yforce','zforce', 'xMag', 'yMag', 'zMag', 'pitch','roll','azimuth']:
                if val in data :
                    s.send(', %6.6f' % data[val])
        s.send(',' + lat + "," + lon)    
        elif name == 'dialog':
            break
    droid.stopSensing()
    s.shutdown(socket.SHUT_RDWR);
    s.close();
    return data["which"]=='negative'
# END

# Prepare the recording session
oldTimeOut=droid.setScreenTimeout(30*60).result;
oldWifi=droid.checkWifiState().result;
if not(oldWifi) :
    droid.toggleWifiState(1)
    time.sleep(15) #wait  for connection to be established

while sendData() :
    pass


#Restore Session
droid.setScreenTimeout(oldTimeOut);
droid.toggleWifiState(oldWifi);

