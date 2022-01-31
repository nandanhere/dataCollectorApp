import csv
from pathlib import Path
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
import csv,os,sys
from datetime import datetime
from time import sleep
from plyer import notification
from pathlib import Path
from plyer import accelerometer,barometer,compass,gps,gravity,gyroscope,humidity,light,proximity,spatialorientation,temperature
import time
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

CLIENT = OSCClient('localhost', 3002)
DEBUG = False
# enable for debug prints
DEBUG = False
sensorList = ["date","time","timestamp","floor","location","accelerometer" , "barometer" , "battery" , "brightness" , "compass" , "gps" ,
     "gravity" , "gyroscope" , "humidity" , "light" , "proximity" , "spatialorientation","temperature" ]
# Create a default dict with default values
global dictList
dictList = []
d = dict.fromkeys(sensorList,"")
def sendNotif():
    pass
    notification.notify(title="Time Table",message=message) #type:ignore
def gps_callback(**kwargs):
    st =  '{lat}:{lon}:{speed}:{bearing}:{altitude}'.format(**kwargs)
    s = st.split(':')
    d['gps'] = {"lat":s[0],"lon":s[1],"speed":s[2],"bearing":s[3],"altitude":s[4]}
            
def updateValues():
    global dictList
    print("updating values")
    try:
        d['accelerometer'] = accelerometer.acceleration #type:ignore
    except:
        print("accelerometer error")
    try:
        d['barometer'] = barometer.pressure #type:ignore
    except:
        print("barometer error")
    try:
        d['battery'] = battery.status #type:ignore
    except:
        print("battery error")
    try:
        d['brightness'] =  brightness.current_level()  #type:ignore WRITE_SETTINGS permisison needed 
    except:
        print("brightness error")
    try:
        d['compass'] =  compass.field_uncalib  #type:ignore you get the uncalibrated field along with iron bias estimation    
    except:
        print("compass error")
    try:
        d['gravity'] =  gravity.gravity #type:ignore
    except:
        print("gravity error")
    try:
        d['gyroscope'] = gyroscope.rotation #type:ignore
    except:
        print("gyroscope error")
    try:
        d['humidity'] = humidity.tell #type:ignore
    except:
        print("humidity error")
    try:
        d['light'] = light.illumination #type:ignore
    except:
        print("light error")
    try:
        d['proximity'] = proximity.proximity #type:ignore
    except:
        print("proximity error")
    try:
        d['spatialorientation'] = spatialorientation.orientation #type:ignore
    except:
        print("spatialorientation error")
    try:
        d['temperature'] = temperature.temperature #type:ignore
    except:
        print("temperature error")
    t = time.time()
    dt = datetime.fromtimestamp(t)
    d["date"] = "date:" + dt.strftime("%d/%m/%Y")
    d["time"] = "time:" + dt.strftime("%H:%M:%S")
    d['timestamp'] = "timestamp : {}".format(time.time())
    try:
        d['battery'] = battery.status #type:ignore BATTERY_STATS permission needed
    except:
        print("battery error")
    dictList.append(d.copy())
def writeData():
    global dictList
    print("Writing data")
    if Path(addr).exists():
          with open(addr,'a') as f: #type:ignore
              csw = csv.DictWriter(f,fieldnames=sensorList)
              for di in dictList:
                csw.writerow(di)
              dictList = []


if __name__ == '__main__':
    dictList = []
    compass.enable() #type:ignore
    accelerometer.enable() #type:ignore
    barometer.enable() #type:ignore
    gyroscope.enable() #type:ignore
    gravity.enable() #type:ignore
    humidity.enable() #type:ignore
    light.enable() #type:ignore
    proximity.enable() #type:ignore
    temperature.enable() #type:ignore
    spatialorientation.enable_listener() #type:ignore
    #   On Android `INTERNET`, `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION` permissions are needed for gps
    gps.configure(on_location=gps_callback) #type:ignore
    gps.start() #type:ignore
    from android.storage import primary_external_storage_path                   #type: ignore     
    dir = primary_external_storage_path()
    download_dir_path = os.path.join(dir, 'Download')                           #type: ignore
    addr = download_dir_path + "/values.csv"
    if not Path(addr).exists():
      with open(addr,'w') as f: #type:ignore
            csw = csv.DictWriter(f,fieldnames=sensorList)
            csw.writeheader()  
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)


    # The getinfo will recieve the floor number and the location of the room/thing.
    def getInfo(message):
        mess = message.decode("utf-8")
        splitt = mess.split(";")
        if DEBUG : print('was pinged with floor data !')
        print(splitt)
        d["floor"] = splitt[0]
        d["location"] = splitt[1]

    
    SERVER.bind(b'/ping',getInfo)
    counter = 0
    while True:
        counter = (counter + 1) % 20
        time.sleep(0.2)
        updateValues()
        if counter == 0:
          writeData()
