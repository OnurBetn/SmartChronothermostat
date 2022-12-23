from PyQt5 import QtCore
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import configparser
import json
import time


class MQTTclient(QtCore.QThread):
    def __init__(self, w):
        QtCore.QThread.__init__(self)
        self.w = w
        self.Connected = False

        self.awsClient = AWSIoTMQTTClient("new_Client")
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

    def callbackL(self, client, userdata, message):
        obj = json.loads(message.payload.decode('utf-8'))
        if obj['source'] != 'rasp':
            self.w.tempSet.setText(str(obj['temp']))

    def callbackK(self, client, userdata, message):
        obj = json.loads(message.payload.decode('utf-8'))
        if obj['source'] != 'rasp':
            self.w.tempSet_2.setText(str(obj['temp']))

    def callbackB(self, client, userdata, message):
        obj = json.loads(message.payload.decode('utf-8'))
        if obj['source'] != 'rasp':
            self.w.tempSet_3.setText(str(obj['temp']))

    def callbackS(self, client, userdata, message):
        obj = json.loads(message.payload.decode('utf-8'))
        if obj['source'] != 'rasp':
            if obj['season'] == 'winter':
                self.w.winter.click()
            else:
                self.w.summer.click()

    def callbackM(self, client, userdata, message):
        obj = json.loads(message.payload.decode('utf-8'))
        if obj['source'] != 'rasp':
            if obj['mode'] == 'auto':
                self.w.autom.click()
            else:
                self.w.manual.click()

    def run(self):
        while self.Connected is not True:  # Wait for connection
            self.awsClient.connect()
            time.sleep(1)

        if self.w.summer.isChecked():
            season = 'winter'
        else:
            season = 'summer'

        if self.w.autom.isChecked():
            mode = 'man'
        else:
            mode = 'auto'

        self.awsClient.subscribe('rooms/living/tempSet', 0, self.callbackL)
        self.awsClient.subscribe('rooms/kitchen/tempSet', 0, self.callbackK)
        self.awsClient.subscribe('rooms/bedroom/tempSet', 0, self.callbackB)
        self.awsClient.subscribe('rooms/season', 0, self.callbackS)
        self.awsClient.subscribe('rooms/mode', 0, self.callbackM)

        while True:
            if self.w.winter.isChecked() and season == 'summer':
                season = 'winter'
                msg = json.dumps({'source': 'rasp', 'season': 'winter'})
                self.awsClient.publish('rooms/season', msg, 0)
            elif self.w.summer.isChecked() and season == 'winter':
                season = 'summer'
                msg = json.dumps({'source': 'rasp', 'season': 'summer'})
                self.awsClient.publish('rooms/season', msg, 0)

            if self.w.autom.isChecked() and mode == 'man':
                mode = 'auto'
                msg = json.dumps({'source': 'rasp', 'mode': 'auto'})
                self.awsClient.publish('rooms/mode', msg, 0)
            elif self.w.manual.isChecked() and mode == 'auto':
                mode = 'man'
                msg = json.dumps({'source': 'rasp', 'mode': 'man'})
                self.awsClient.publish('rooms/mode', msg, 0)

            time.sleep(1)

    def on_online(self):
        self.Connected = True
