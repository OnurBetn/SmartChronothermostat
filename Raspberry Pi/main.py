from PyQt5 import uic, QtWidgets, QtCore, QtGui
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import paho.mqtt.client as mqtt
import Adafruit_DHT as dht
import schedule
import settings
import standby
import awsmqtt
import awscloud
import configparser
import requests
import sys
import time
import json


class SendValues(QtCore.QThread):
    def __init__(self, w):
        QtCore.QThread.__init__(self)
        self.w = w
        self.Connected = False

        self.awsClient = AWSIoTMQTTClient("new_pub01")
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.awsClient.configureEndpoint(config['mqttbroker']['ip'], int(config['mqttbroker']['port']))
        self.awsClient.configureCredentials("./certificates/AmazonRootCA1.pem",
                                            "./certificates/9d3ae4ef02-private.pem.key",
                                            "./certificates/9d3ae4ef02-certificate.pem.crt")
        self.awsClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.awsClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.awsClient.configureConnectDisconnectTimeout(10)
        self.awsClient.configureMQTTOperationTimeout(5)
        self.awsClient.onOnline = self.on_online

    def run(self):
        while self.Connected is not True:  # Wait for connection
            self.awsClient.connect()
            time.sleep(1)
        while True:
            msg = json.dumps({'source': 'rasp',
                              'temperature': float(self.w.tempReal.text()),
                              'humidity': float(self.w.humidity_6.text()[0:-1])})
            self.awsClient.publish('rooms/living/TempHum', msg, 0)

            msg = json.dumps({'source': 'rasp',
                              'temperature': float(self.w.tempReal_2.text()),
                              'humidity': float(self.w.humidity_7.text()[0:-1])})
            self.awsClient.publish('rooms/kitchen/TempHum', msg, 0)

            msg = json.dumps({'source': 'rasp',
                              'temperature': float(self.w.tempReal_3.text()),
                              'humidity': float(self.w.humidity_8.text()[0:-1])})
            self.awsClient.publish('rooms/bedroom/TempHum', msg, 0)
            time.sleep(10)

    def on_online(self):
        self.Connected = True


class GetValues(QtCore.QThread):
    def __init__(self, w):
        QtCore.QThread.__init__(self)
        self.w = w

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.messageBroker = config['localmqtt']['ip']
        self.port = int(config['localmqtt']['port'])

        self.connected_flag = False  # create flag in class
        self.client = mqtt.Client("Python")  # create new instance
        self.client.on_connect = self.on_connect  # attach function to callback
        self.client.on_message = self.on_message  # attach function to callback
        self.client.connect(self.messageBroker, port=self.port)  # connect to broker
        self.client.loop_start()  # start the loop

    def run(self):
        while True:
            h, t = dht.read_retry(dht.DHT22, 25)
            self.w.tempReal.setText(str(round(t * 2) / 2))
            self.w.humidity_6.setText(str(round(h * 2) / 2) + '%')
            time.sleep(10)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to local broker")
            self.client.subscribe([("rooms/kitchen/values", 0), ("rooms/bedroom/values", 0)])
            self.connected_flag = True
        else:
            print("Connection to local broker failed")

    def on_message(self, client, userdata, message):
        obj = json.loads(message.payload.decode())
        if message.topic == "rooms/kitchen/values":
            self.w.tempReal_2.setText(str(round(obj['temperature'] * 2) / 2))
            self.w.humidity_7.setText(str(round(obj['humidity'] * 2) / 2) + '%')
        elif message.topic == "rooms/bedroom/values":
            self.w.tempReal_3.setText(str(round(obj['temperature'] * 2) / 2))
            self.w.humidity_8.setText(str(round(obj['humidity'] * 2) / 2) + '%')


class CheckTemp(QtCore.QThread):
    def __init__(self, w):
        QtCore.QThread.__init__(self)
        self.w = w
        self.runs = True

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.messageBroker = config['localmqtt']['ip']
        self.port = int(config['localmqtt']['port'])

        self.connected_flag = False  # create flag in class
        self.client = mqtt.Client("Python1")  # create new instance
        self.client.on_connect = self.on_connect  # attach function to callback
        self.client.connect(self.messageBroker, port=self.port)  # connect to broker

        self.client.loop_start()  # start the loop

    def run(self):
        self.runs = True
        while self.runs:
            if self.w.winter.isChecked():
                pixmap = QtGui.QPixmap('./images/heater.png')
                self.w.status.setPixmap(pixmap)
                self.w.status_2.setPixmap(pixmap)
                self.w.status_3.setPixmap(pixmap)
                self.winter()
            elif self.w.summer.isChecked():
                pixmap = QtGui.QPixmap('./images/cooler.png')
                self.w.status.setPixmap(pixmap)
                self.w.status_2.setPixmap(pixmap)
                self.w.status_3.setPixmap(pixmap)
                self.summer()
            time.sleep(1)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to local broker")
            self.connected_flag = True
        else:
            print("Connection to local broker failed")

    def stop(self):
        self.runs = False

    def winter(self):
        # Check living room
        if float(self.w.tempReal.text()) < (float(self.w.tempSet.text()) - float(self.w.Hyst.text())):
            # Accendo il relay
            self.client.publish('rooms/living/relay', 'ON', 0)

            self.w.status.setVisible(True)
            time.sleep(2)
            self.w.status.setVisible(False)
            time.sleep(2)
        if float(self.w.tempReal.text()) > (float(self.w.tempSet.text()) + float(self.w.Hyst.text())):
            # Spengo il relay
            self.client.publish('rooms/living/relay', 'OFF', 0)
            self.w.status.setVisible(False)

        # Check kitchen
        if float(self.w.tempReal_2.text()) < (float(self.w.tempSet_2.text()) - float(self.w.Hyst.text())):
            # Accendo il relay
            self.client.publish('rooms/kitchen/relay', 'ON', 0)

            self.w.status_2.setVisible(True)
            time.sleep(2)
            self.w.status_2.setVisible(False)
            time.sleep(2)
        if float(self.w.tempReal_2.text()) > (float(self.w.tempSet_2.text()) + float(self.w.Hyst.text())):
            # Spengo il relay
            self.client.publish('rooms/kitchen/relay', 'OFF', 0)
            self.w.status_2.setVisible(False)

        # Check bedroom
        if float(self.w.tempReal_3.text()) < (float(self.w.tempSet_3.text()) - float(self.w.Hyst.text())):
            # Accendo il relay
            self.client.publish('rooms/bedroom/relay', 'ON', 0)

            self.w.status_3.setVisible(True)
            time.sleep(2)
            self.w.status_3.setVisible(False)
            time.sleep(2)
        if float(self.w.tempReal_3.text()) > (float(self.w.tempSet_3.text()) + float(self.w.Hyst.text())):
            # Spengo il relay
            self.client.publish('rooms/bedroom/relay', 'OFF', 0)
            self.w.status_3.setVisible(False)

    def summer(self):
        # Check living room
        if float(self.w.tempReal.text()) > float(self.w.tempSet.text()) + float(self.w.Hyst.text()):
            # Air conditioner ON
            self.client.publish('rooms/living/conditioner', 'ON', 0)

            self.w.status.setVisible(True)
            time.sleep(2)
            self.w.status.setVisible(False)
            time.sleep(2)
        if float(self.w.tempReal.text()) < float(self.w.tempSet.text()) - float(self.w.Hyst.text()):
            # Air conditioner OFF
            self.client.publish('rooms/living/conditioner', 'OFF', 0)
            self.w.status.setVisible(False)

        # Check kitchen
        if float(self.w.tempReal_2.text()) > (float(self.w.tempSet_2.text()) - float(self.w.Hyst.text())):
            # Accendo il relay
            self.client.publish('rooms/kitchen/conditioner', 'ON', 0)

            self.w.status_2.setVisible(True)
            time.sleep(2)
            self.w.status_2.setVisible(False)
            time.sleep(2)
        if float(self.w.tempReal_2.text()) < (float(self.w.tempSet_2.text()) + float(self.w.Hyst.text())):
            # Spengo il relay
            self.client.publish('rooms/kitchen/conditioner', 'OFF', 0)
            self.w.status_2.setVisible(False)

        # Check bedroom
        if float(self.w.tempReal_3.text()) > (float(self.w.tempSet_3.text()) - float(self.w.Hyst.text())):
            # Accendo il relay
            self.client.publish('rooms/bedroom/conditioner', 'ON', 0)

            self.w.status_3.setVisible(True)
            time.sleep(2)
            self.w.status_3.setVisible(False)
            time.sleep(2)
        if float(self.w.tempReal_3.text()) < (float(self.w.tempSet_3.text()) + float(self.w.Hyst.text())):
            # Spengo il relay
            self.client.publish('rooms/bedroom/conditioner', 'OFF', 0)
            self.w.status_3.setVisible(False)


class AutoMode(QtCore.QThread):
    def __init__(self, w):
        QtCore.QThread.__init__(self)
        self.w = w
        self.runs = True

    def run(self):
        self.runs = True
        while self.runs:
            f = open('schedule_living.json', 'r')
            obj = json.loads(f.read())
            self.w.tempSet.setText(obj[time.strftime("%a")][int(time.strftime("%H")) - 1])
            f.close()

            f = open('schedule_kitchen.json', 'r')
            obj = json.loads(f.read())
            self.w.tempSet_2.setText(obj[time.strftime("%a")][int(time.strftime("%H")) - 1])
            f.close()

            f = open('schedule_bedroom.json', 'r')
            obj = json.loads(f.read())
            self.w.tempSet_3.setText(obj[time.strftime("%a")][int(time.strftime("%H")) - 1])
            f.close()

            time.sleep(2)

    def stop(self):
        self.runs = False


class ShowDate(QtCore.QThread):
    def __init__(self, w):
        QtCore.QThread.__init__(self)
        self.w = w

    def run(self):
        while True:
            self.w.date.setText(time.strftime("%a, %d %B %Y"))
            self.w.time.setText(time.strftime("%H:%M"))
            time.sleep(1)


class ShowWeather(QtCore.QThread):
    def __init__(self, w):
        QtCore.QThread.__init__(self)
        self.w = w

    def run(self):
        api_key = self.get_key()
        while True:
            try:
                location = str(self.w.location.text())
                weather = self.get_weather(api_key, location)
                pixmap = QtGui.QPixmap('./images/weather/'+weather['weather'][0]['icon']+'.png')
                self.w.weathIcon.setPixmap(pixmap)
                self.w.condition.setText(weather['weather'][0]['main'])
                self.w.outTemp.setText(str(round(weather['main']['temp'] * 2) / 2))
                self.w.location.setText(weather['name'])
                self.w.outHum.setText(str(weather['main']['humidity']) + '%')
                time.sleep(5)
            except:
                self.w.condition.setText("Not available")
                self.w.outTemp.setText("X")
                self.w.location.setText("Not available")
                self.w.outHum.setText("X")
                time.sleep(5)

    @staticmethod
    def get_key():
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config['openweathermap']['api']

    @staticmethod
    def get_weather(api_key, location):
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, api_key)
        r = requests.get(url)
        return r.json()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.Hyst.setVisible(False)

        # Threads
        self.autoMode = AutoMode(self)
        self.getWeatherThread = ShowWeather(self)
        self.getWeatherThread.start()
        self.getDateThread = ShowDate(self)
        self.getDateThread.start()
        self.checkTempThread = CheckTemp(self)
        self.checkTempThread.start()
        self.showTempThread = GetValues(self)
        self.showTempThread.start()
        self.sendTemp = SendValues(self)
        self.sendTemp.start()
        self.mqtt_client = awsmqtt.MQTTclient(self)
        self.mqtt_client.start()
        self.mqtt_cloud = awscloud.MQTTcloud(self)
        self.mqtt_cloud.start()

        # Signals
        self.autom.clicked.connect(self.auto)
        self.manual.clicked.connect(self.man)
        self.buttonUP.clicked.connect(self.tempUp)
        self.buttonDOWN.clicked.connect(self.tempDown)
        self.buttonUP_2.clicked.connect(self.tempUp_2)
        self.buttonDOWN_2.clicked.connect(self.tempDown_2)
        self.buttonUP_3.clicked.connect(self.tempUp_3)
        self.buttonDOWN_3.clicked.connect(self.tempDown_3)
        self.schedule.clicked.connect(self.showSched)
        self.settings.clicked.connect(self.showSett)
        self.buttonRight.clicked.connect(lambda: self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() + 1) % 3))
        self.buttonLeft.clicked.connect(lambda: self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() - 1) % 3))
        self.buttonONOFF.clicked.connect(self.energySave)
        self.status.setVisible(False)
        self.status_2.setVisible(False)
        self.status_3.setVisible(False)

        # AWS Client
        self.awsClient = AWSIoTMQTTClient("new_pub")
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.awsClient.configureEndpoint(config['mqttbroker']['ip'], int(config['mqttbroker']['port']))
        self.awsClient.configureCredentials("./certificates/AmazonRootCA1.pem",
                                            "./certificates/9d3ae4ef02-private.pem.key",
                                            "./certificates/9d3ae4ef02-certificate.pem.crt")
        self.awsClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.awsClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.awsClient.configureConnectDisconnectTimeout(10)
        self.awsClient.configureMQTTOperationTimeout(5)
        self.awsClient.connect()

    def auto(self):
        self.buttonUP.setEnabled(False)
        self.buttonDOWN.setEnabled(False)
        self.buttonUP_2.setEnabled(False)
        self.buttonDOWN_2.setEnabled(False)
        self.buttonUP_3.setEnabled(False)
        self.buttonDOWN_3.setEnabled(False)

        self.autoMode.start()

    def man(self):
        self.buttonUP.setEnabled(True)
        self.buttonDOWN.setEnabled(True)
        self.buttonUP_2.setEnabled(True)
        self.buttonDOWN_2.setEnabled(True)
        self.buttonUP_3.setEnabled(True)
        self.buttonDOWN_3.setEnabled(True)

        self.autoMode.stop()

    def tempUp(self):
        if float(self.tempSet.text()) < 30:
            temp = float(self.tempSet.text()) + 0.5
            self.tempSet.setText(str(temp))

            msg = json.dumps({'source': 'rasp', 'temp': float(self.tempSet.text())})
            self.awsClient.publish('rooms/living/tempSet', msg, 0)

    def tempDown(self):
        if float(self.tempSet.text()) > 5:
            temp = float(self.tempSet.text()) - 0.5
            self.tempSet.setText(str(temp))

            msg = json.dumps({'source': 'rasp', 'temp': float(self.tempSet.text())})
            self.awsClient.publish('rooms/living/tempSet', msg, 0)

    def tempUp_2(self):
        if float(self.tempSet_2.text()) < 30:
            temp = float(self.tempSet_2.text()) + 0.5
            self.tempSet_2.setText(str(temp))

            msg = json.dumps({'source': 'rasp', 'temp': float(self.tempSet_2.text())})
            self.awsClient.publish('rooms/kitchen/tempSet', msg, 0)

    def tempDown_2(self):
        if float(self.tempSet_2.text()) > 5:
            temp = float(self.tempSet_2.text()) - 0.5
            self.tempSet_2.setText(str(temp))

            msg = json.dumps({'source': 'rasp', 'temp': float(self.tempSet_2.text())})
            self.awsClient.publish('rooms/kitchen/tempSet', msg, 0)

    def tempUp_3(self):
        if float(self.tempSet_3.text()) < 30:
            temp = float(self.tempSet_3.text()) + 0.5
            self.tempSet_3.setText(str(temp))

            msg = json.dumps({'source': 'rasp', 'temp': float(self.tempSet_3.text())})
            self.awsClient.publish('rooms/bedroom/tempSet', msg, 0)

    def tempDown_3(self):
        if float(self.tempSet_3.text()) > 5:
            temp = float(self.tempSet_3.text()) - 0.5
            self.tempSet_3.setText(str(temp))

            msg = json.dumps({'source': 'rasp', 'temp': float(self.tempSet_3.text())})
            self.awsClient.publish('rooms/bedroom/tempSet', msg, 0)

    def energySave(self):
        self.setEnabled(False)
        energy = standby.EnergySave(self)
        self.checkTempThread.stop()
        energy.showFullScreen()
        energy.exec_()

    def showSched(self):
        self.setEnabled(False)
        sched = schedule.Schedule(self)
        sched.showFullScreen()
        sched.exec_()

    def showSett(self):
        self.setEnabled(False)
        sett = settings.Settings(self)
        sett.show()
        sett.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.showFullScreen()
    sys.exit(app.exec_())
