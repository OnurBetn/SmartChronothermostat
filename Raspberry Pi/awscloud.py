from PyQt5 import QtCore
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import datetime


class MQTTcloud(QtCore.QThread):
    def __init__(self, w):
        QtCore.QThread.__init__(self)
        self.w = w
        self.Connected = False

        self.awsCloud = AWSIoTMQTTClient("pl19-03")
        self.awsCloud.configureEndpoint("a3cezb6rg1vyed-ats.iot.us-west-2.amazonaws.com", 8883)
        self.awsCloud.configureCredentials("./cloud_cert/root-CA.crt",
                                           "./cloud_cert/PL-student.private.key",
                                           "./cloud_cert/PL-student.cert.pem")
        self.awsCloud.configureAutoReconnectBackoffTime(1, 32, 20)
        self.awsCloud.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.awsCloud.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.awsCloud.configureConnectDisconnectTimeout(10)
        self.awsCloud.configureMQTTOperationTimeout(5)
        self.awsCloud.onOnline = self.on_online
        self.awsCloud.subscribe("pl19/notification", 1, self.customCallback)

    def run(self):
        while self.Connected is not True:  # Wait for connection
            self.awsCloud.connect()
            time.sleep(1)

        MAC = "12:34:56:78:90:AA"

        tempLiving = float(self.w.tempSet.text())
        tempKitchen = float(self.w.tempSet_2.text())
        tempBedroom = float(self.w.tempSet_3.text())

        if self.w.summer.isChecked():
            season = 'winter'
        else:
            season = 'summer'

        if self.w.autom.isChecked():
            mode = 'man'
        else:
            mode = 'auto'
        while True:
            if tempLiving != float(self.w.tempSet.text()):
                tempLiving = float(self.w.tempSet.text())
                event = {'room': "Living Room",
                         'temperature': float(self.w.tempSet.text()),
                         'message': "Target Temp Changed!"}

                message = {'device_mac': MAC,
                           'timestamp': str(datetime.datetime.now()),
                           'event_id': 2,
                           'event': event}
                self.awsCloud.publish('pl19/event', json.dumps(message), 1)

            if tempKitchen != float(self.w.tempSet_2.text()):
                tempKitchen = float(self.w.tempSet_2.text())
                event = {'room': "Kitchen",
                         'temperature': float(self.w.tempSet_2.text()),
                         'message': "Target Temp Changed!"}

                message = {'device_mac': MAC,
                           'timestamp': str(datetime.datetime.now()),
                           'event_id': 2,
                           'event': event}
                self.awsCloud.publish('pl19/event', json.dumps(message), 1)

            if tempBedroom != float(self.w.tempSet_3.text()):
                tempBedroom = float(self.w.tempSet_3.text())
                event = {'room': "Bedroom",
                         'temperature': float(self.w.tempSet_3.text()),
                         'message': "Target Temp Changed!"}

                message = {'device_mac': MAC,
                           'timestamp': str(datetime.datetime.now()),
                           'event_id': 2,
                           'event': event}
                self.awsCloud.publish('pl19/event', json.dumps(message), 1)

            if self.w.winter.isChecked() and season == 'summer':
                season = 'winter'
                event = {'message': "Winter profile active!"}

                message = {'device_mac': MAC,
                           'timestamp': str(datetime.datetime.now()),
                           'event_id': 3,
                           'event': event}
                self.awsCloud.publish('pl19/event', json.dumps(message), 1)

            elif self.w.summer.isChecked() and season == 'winter':
                season = 'summer'
                event = {'message': "Summer profile active!"}

                message = {'device_mac': MAC,
                           'timestamp': str(datetime.datetime.now()),
                           'event_id': 3,
                           'event': event}
                self.awsCloud.publish('pl19/event', json.dumps(message), 1)

            if self.w.autom.isChecked() and mode == 'man':
                mode = 'auto'
                event = {'message': "Auto mode active!"}

                message = {'device_mac': MAC,
                           'timestamp': str(datetime.datetime.now()),
                           'event_id': 3,
                           'event': event}
                self.awsCloud.publish('pl19/event', json.dumps(message), 1)

            elif self.w.manual.isChecked() and mode == 'auto':
                mode = 'man'
                event = {'message': "Manual mode active!"}

                message = {'device_mac': MAC,
                           'timestamp': str(datetime.datetime.now()),
                           'event_id': 3,
                           'event': event}
                self.awsCloud.publish('pl19/event', json.dumps(message), 1)

            time.sleep(1)

    def on_online(self):
        self.Connected = True

    def replyToPing(self, sequence):
        pingData = {}

        pingData['sequence'] = sequence
        pingData['message'] = "Ping response."

        message = {}
        message['device_mac'] = "12:34:56:78:90:AA"
        message['timestamp'] = str(datetime.datetime.now())
        message['event_id'] = 1
        message['event'] = pingData
        messageJson = json.dumps(message)
        self.awsCloud.publishAsync("pl19/event", messageJson, 1)

    # Custom MQTT message callback
    def customCallback(self, client, userdata, message):
        print("Received a new message: ")
        messageContent = json.loads(message.payload.decode('utf-8'))
        messageData = messageContent['event']
        print(messageContent)
        print(messageData['message'])
        print("Sequence ", messageData['sequence'])
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")
        if messageContent['event_id'] == 0:
            self.replyToPing(messageData['sequence'])
