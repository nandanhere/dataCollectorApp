from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
import platform
from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
import time,datetime
from plyer import accelerometer,barometer,brightness,battery,compass,gps,gravity,gyroscope,humidity,light,proximity,spatialorientation,temperature
from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer
from kivy.utils import platform
from kivy.lang import Builder
# comment this if you are running on computer
from jnius import autoclass
sensorList = sorted(["date","time","timestamp","floor","location","accelerometer" , "barometer" , "battery" , "brightness" , "compass" , "gps" ,
     "gravity" , "gyroscope" , "humidity" , "light" , "proximity" , "spatialorientation","temperature" ])

Builder.load_string(
    '''
#:import images_path kivymd.images_path


<CustomOneLineIconListItem>

    ThreeLineListItem:
        text: "Three-line"


<HomeScreen>

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)

        MDBoxLayout:
            adaptive_height: True
            MDTextField:
                id: floor
                hint_text: 'Enter the Floor'
                on_text_validate: root.ids.location.focus = True
        MDBoxLayout:
            adaptive_height: True
            MDTextField:
                id: location
                hint_text: 'Enter the location'
                on_text_validate: root.submit()
        MDBoxLayout:
            adaptive_height: True
            MDFlatButton:
                id: submitbutton
                text: "Enter Room and floor number"
                increment_width: "300dp"
                on_press: root.submit()
                background_color: (0.5, 0.7, 0.5, 0.9)   

        RecycleView:
            id: rv
            key_viewclass: 'viewclass'
            key_size: 'height'

            RecycleBoxLayout:
                padding: dp(10)
                default_size: None, dp(100)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
'''
)

 

class HomeScreen(Screen):
    def __init__(self,client, **kw):
        super().__init__(**kw)
        self.sensorLabelList = {}
        self.gpstext = ""
        self.client = client
        try: 
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
            gps.configure(on_location=self.gps_callback) #type:ignore
            gps.start() #type:ignore
        except Exception as ex: print("Error :", ex)
        Clock.schedule_interval(self.clockFn, 3)

    def gps_callback(self,**kwargs):
            self.gpstext =  'lat: {lat}, lon: {lon},speed:{speed},bearing:{bearing},altitude:{altitude}'.format(**kwargs)
    def submit(self):
        floor,location = self.ids.floor.text,self.ids.location.text
        print("the inputs are " , self.ids.floor.text, self.ids.location.text)
        self.ids.submitbutton.text = "Floor : " + self.ids.floor.text + " Location: " + self.ids.location.text
        self.ids.rv.data[self.sensorLabelList['floor']]['secondary_text'] = self.ids.floor.text
        self.ids.rv.data[self.sensorLabelList['location']]['secondary_text'] = self.ids.location.text
        ss = "{};{}".format(floor,location)
        message = bytes(ss,'utf-8')
        print(message)
        self.client.send_message(b'/ping', [message,])

    def clockFn(self,dt):
        try: self.ids.rv.data[self.sensorLabelList["accelerometer"]]['secondary_text'] = str(accelerometer.acceleration)
        except Exception as ex: print("accelerometer Error :", ex)
        try: self.ids.rv.data[self.sensorLabelList['barometer']]['secondary_text'] = str(barometer.pressure)
        except Exception as ex: print("barometer Error :", ex)
        try: self.ids.rv.data[self.sensorLabelList['brightness']]['secondary_text'] = str(brightness.current_level()) #type:ignore WRITE_SETTINGS permisison needed 
        except Exception as ex: print("brightness Error :", ex)
        try: self.ids.rv.data[self.sensorLabelList['compass']]['secondary_text'] = str(compass.field_uncalib) #type:ignore you get the uncalibrated field along with iron bias estimation
        except Exception as ex: print("compass Error :", ex)
        #   On Android `INTERNET`, `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION` permissions are needed for gps

        try: self.ids.rv.data[self.sensorLabelList['gps']]['secondary_text'] = self.gpstext
        except Exception as ex: print("gps Error :", ex)
        try: self.ids.rv.data[self.sensorLabelList['gravity']]['secondary_text'] = str(gravity.gravity) #type:ignore
        except Exception as ex: print("gravity Error :", ex)
        try: self.ids.rv.data[self.sensorLabelList['gyroscope']]['secondary_text'] = str(gyroscope.rotation)
        except Exception as ex: print("gyroscope Error :", ex)
        try:self.sensorLabelList['humidity'].text = "humidity : {}".format(humidity.tell) #type:ignore
        except Exception as ex: print("humidity Error :", ex)
        try: self.ids.rv.data[self.sensorLabelList['light']]['secondary_text'] = str(light.illumination) #type:ignore
        except Exception as ex: print("light Error :", ex)
        try: self.ids.rv.data[self.sensorLabelList['proximity']]['secondary_text'] = str(proximity.proximity) #type:ignore
        except Exception as ex: print("proximity Error :", ex)
        try:self.ids.rv.data[self.sensorLabelList['spatialorientation']]['secondary_text'] = str(spatialorientation.orientation) #type:ignore
        except Exception as ex: print("spatialorientation Error :", ex)
        try: self.ids.rv.data[self.sensorLabelList['temperature']]['secondary_text'] = str(temperature.temperature) #type:ignore
        except Exception as ex: print("temperature Error :", ex)
        try : self.ids.rv.data[self.sensorLabelList['battery']]['secondary_text'] = str(battery.status) #BATTERY_STATS permission needed
        except Exception as ex: print("battery Error :", ex)
        

        t = time.time()
        dt = datetime.datetime.fromtimestamp(t)
        self.ids.rv.data[self.sensorLabelList['date']]['secondary_text'] = dt.strftime("%d/%m/%Y")
        self.ids.rv.data[self.sensorLabelList['time']]['secondary_text'] = dt.strftime("%H:%M:%S")
        self.ids.rv.data[self.sensorLabelList['timestamp']]['secondary_text'] = str(time.time())
        self.ids.rv.refresh_from_data()

    def buildlist(self):
        self.sensorLabelList = {}
        i = 0
        for id in sensorList:
            self.ids.rv.data.append(
                {
                    "viewclass": "ThreeLineListItem",
                    "id": id,
                    "text": id,
                    "secondary_text": self.sensorLabelList.get(id,"None"), #type:ignore
                }
            )
            self.sensorLabelList[id] = i
            i += 1


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.server = server = OSCThreadServer()
        server.listen(
                address=b'localhost',
                port=3002,
                default=True,
            )
        server.bind(b'/message', self.callback)
        self.client = OSCClient(b'localhost', 3000)
        if platform == 'android':
            SERVICE_NAME = u'{packagename}.Service{servicename}'.format(packagename=u'org.kivy.datacollector',servicename=u'Datacollectorservice')
            service = autoclass(SERVICE_NAME)
            self.mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
            argument = ''
            service.start(self.mActivity, argument)
            self.service = service
        self.screen = HomeScreen(self.client)

    def build(self):
        return self.screen
    def callback(self):
        # Not needed in this program. added just in case its needed in the future
        pass

    def on_start(self):
        self.screen.buildlist()



if __name__=='__main__':
    if platform == "android":
        from android.permissions import request_permissions,Permission,check_permission            #type: ignore
        # since service needs these perms we need to ask through ui 
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE,Permission.WRITE_SETTINGS,Permission.ACCESS_FINE_LOCATION,Permission.ACCESS_COARSE_LOCATION])
        
    MainApp().run()
