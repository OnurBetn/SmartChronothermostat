from PyQt5 import uic, QtWidgets, QtCore
import wifi
import requests
import subprocess
import os
import time


def Search():
    wifilist = []

    cells = wifi.Cell.all('wlan0')

    for cell in cells:
        wifilist.append(cell)

    return wifilist


def FindFromSearchList(ssid):
    wifilist = Search()

    for cell in wifilist:
        if cell.ssid == ssid:
            return cell

    return False


def FindFromSavedList(ssid):
    cell = wifi.Scheme.find('wlan0', ssid)

    if cell:
        return cell

    return False

def Add(cell, password=None):
    if not cell:
        return False

    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    scheme.save()
    return scheme


def Delete(ssid):
    if not ssid:
        return False

    cell = FindFromSavedList(ssid)

    if cell:
        cell.delete()
        return True

    return False


class Settings(QtWidgets.QDialog):
    def __init__(self, w):
        super(Settings, self).__init__()
        self.w = w
        uic.loadUi('settings.ui', self)
        self.Saved.setVisible(False)
        self.Connected.setVisible(False)
        self.Hyst.setText(str(self.w.Hyst.text()))
        self.lineEdit.setText(str(self.w.location.text()))

        self.treeWidget.setColumnWidth(0, 50)
        self.treeWidget.setColumnWidth(1, 200)
        self.treeWidget.setColumnWidth(2, 50)
        self.scan()

        self.buttonUP.clicked.connect(self.hystUp)
        self.buttonDOWN.clicked.connect(self.hystDown)
        self.save.clicked.connect(self.saveSett)
        self.connect.clicked.connect(self.connectWifi)
        self.back.clicked.connect(self.closeW)
        self.treeWidget.itemSelectionChanged.connect(self.itemSelected)
        self.getLoc.clicked.connect(self.getLocation)
        self.passvisible.pressed.connect(lambda: self.password.setEchoMode(QtWidgets.QLineEdit.Normal))
        self.passvisible.released.connect(lambda: self.password.setEchoMode(QtWidgets.QLineEdit.Password))
        self.lineEdit.focusInEvent = self.openKeyboard
        self.lineEdit.focusOutEvent = self.closeKeyboard
        self.password.focusInEvent = self.openKeyboard
        self.password.focusOutEvent = self.closeKeyboard
        self.refreshWifi.clicked.connect(self.scan)

        timer = QtCore.QTimer(self)
        timer.setInterval(1)
        timer.setSingleShot(True)
        timer.timeout.connect(self.fakeMaximize)
        timer.start()

    def itemSelected(self):
        self.ssidlabel.setText(str(self.treeWidget.currentItem().text(1)))
        self.connect.setEnabled(True)

    def fakeMaximize(self):
        os.system('xprop -name Dialog -f _MOTIF_WM_HINTS 32c -set _MOTIF_WM_HINTS "0x2, 0x0, 0x0, 0x0, 0x0"')
        os.system('wmctrl -r Dialog -e 0,0,0,-1,-1')

    def closeW(self):
        self.close()
        self.w.setEnabled(True)

    def openKeyboard(self, e):
        try:
            subprocess.Popen(["matchbox-keyboard"])
            time.sleep(0.1)
            os.system('wmctrl -r Keyboard -b add,above')
            os.system('xprop -name Keyboard -f _MOTIF_WM_HINTS 32c -set _MOTIF_WM_HINTS "0x2, 0x0, 0x0, 0x0, 0x0"')
            os.system('wmctrl -r Keyboard -e 0,0,0,-1,-1')
        except FileNotFoundError:
            pass

    def closeKeyboard(self, e):
        subprocess.Popen(["killall", "matchbox-keyboard"])

    def getLocation(self):
        try:
            url = "https://ipinfo.io/json"
            r = requests.get(url)
            self.lineEdit.setText(r.json()['city'])
        except:
            print('Error in getting location!')

    def scan(self):
        self.treeWidget.clear()
        for cell in wifi.Cell.all('wlan0'):
            exist = False
            for j in range(self.treeWidget.topLevelItemCount()):
                index = self.treeWidget.topLevelItem(j)
                strg = index.text(1)
                if strg == cell.ssid:
                    exist = True
                    break
            if not exist:
                item = QtWidgets.QTreeWidgetItem()
                item.setTextAlignment(0, QtCore.Qt.AlignHCenter)
                item.setTextAlignment(1, QtCore.Qt.AlignHCenter)
                item.setTextAlignment(2, QtCore.Qt.AlignHCenter)
                item.setText(0, str(cell.signal))
                item.setText(1, cell.ssid)
                item.setText(2, cell.encryption_type)
                self.treeWidget.addTopLevelItem(item)

    def hystUp(self):
        if float(self.Hyst.text()) < 5:
            temp = float(self.Hyst.text()) + 0.5
            self.Hyst.setText(str(temp))
            self.save.setEnabled(True)

    def hystDown(self):
        if float(self.Hyst.text()) > 0:
            temp = float(self.Hyst.text()) - 0.5
            self.Hyst.setText(str(temp))
            self.save.setEnabled(True)

    def saveSett(self):
        timer = QtCore.QTimer(self)
        self.save.setEnabled(False)
        self.Saved.setVisible(True)
        timer.setInterval(2000)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.Saved.setVisible(False))
        timer.start()

        self.w.Hyst.setText(str(self.Hyst.text()))
        self.w.location.setText(str(self.lineEdit.text()))

    def connectWifi(self):
        ssid = self.ssidlabel.text()
        password = self.password.text()
        cell = FindFromSearchList(ssid)

        if cell:
            savedcell = FindFromSavedList(cell.ssid)

            # Already Saved from Setting
            if savedcell:
                savedcell.activate()

            # First time to conenct
            else:
                if cell.encrypted:
                    if password is not '':
                        #scheme = Add(cell, password)

                        # Wrong Password
                        self.Connected.setText('Wrong Password!')
                        Delete(ssid)

                    else:
                        self.Connected.setText('Insert Password!')

                else:
                    #scheme = Add(cell)
                    self.Connected.setText('Error!')
                    Delete(ssid)

        timer = QtCore.QTimer(self)
        self.connect.setEnabled(False)
        self.Connected.setVisible(True)
        timer.setInterval(2000)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.Connected.setVisible(False))
        timer.start()

