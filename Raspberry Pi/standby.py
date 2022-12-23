from PyQt5 import uic, QtWidgets, QtCore
import time


class AntiFreeze(QtCore.QThread):
    def __init__(self, w, main):
        QtCore.QThread.__init__(self)
        self.w = w
        self.main = main

    def run(self):
        while True:
            if float(self.main.tempReal.text()) < 5:
                # Accendo il relay

                pass
            else:
                # Spengo il relay

                pass
            time.sleep(120)


class ShowDate(QtCore.QThread):
    def __init__(self, w):
        QtCore.QThread.__init__(self)
        self.w = w

    def run(self):
        while True:
            self.w.date.setText(time.strftime("%a, %d %B %Y"))
            self.w.time.setText(time.strftime("%H:%M"))
            time.sleep(1)


class EnergySave(QtWidgets.QDialog):
    def __init__(self, w):
        super(EnergySave, self).__init__()
        uic.loadUi('standby.ui', self)
        self.w = w
        self.getDateThread = ShowDate(self)
        self.getDateThread.start()
        self.antiFreeze = AntiFreeze(self, w)
        self.antiFreeze.start()

        self.button.clicked.connect(self.restart)

    def restart(self):
        self.close()
        self.w.setEnabled(True)
        self.w.checkTempThread.start()
