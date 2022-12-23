from PyQt5 import uic, QtWidgets, QtCore
import json


class Schedule(QtWidgets.QDialog):
    def __init__(self, w):
        super(Schedule, self).__init__()
        uic.loadUi('schedule.ui', self)
        self.w = w
        self.Saved.setVisible(False)

        self.buttonRight.clicked.connect(
            lambda: self.changeZone.setCurrentIndex((self.changeZone.currentIndex() + 1) % 3))
        self.buttonLeft.clicked.connect(
            lambda: self.changeZone.setCurrentIndex((self.changeZone.currentIndex() - 1) % 3))

        self.MON.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.TUE.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.WED.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.THU.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.FRI.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.SAT.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.SUN.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))

        self.MON_2.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(0))
        self.TUE_2.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(1))
        self.WED_2.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(2))
        self.THU_2.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(3))
        self.FRI_2.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(4))
        self.SAT_2.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(5))
        self.SUN_2.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(6))

        self.MON_3.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(0))
        self.TUE_3.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(1))
        self.WED_3.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(2))
        self.THU_3.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(3))
        self.FRI_3.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(4))
        self.SAT_3.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(5))
        self.SUN_3.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(6))

        for t in self.findChildren(QtWidgets.QTableWidget):
            t.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            t.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.save.setEnabled(False)
        self.save.clicked.connect(self.writeJson)
        self.back.clicked.connect(self.closeW)

        self.bUP.clicked.connect(self.tempUP)
        self.bUP2.clicked.connect(self.tempUP2)
        self.bUP3.clicked.connect(self.tempUP3)
        self.bUP4.clicked.connect(self.tempUP4)
        self.bUP5.clicked.connect(self.tempUP5)
        self.bUP6.clicked.connect(self.tempUP6)
        self.bUP7.clicked.connect(self.tempUP7)

        self.bUP_2.clicked.connect(self.tempUP_2)
        self.bUP2_2.clicked.connect(self.tempUP2_2)
        self.bUP3_2.clicked.connect(self.tempUP3_2)
        self.bUP4_2.clicked.connect(self.tempUP4_2)
        self.bUP5_2.clicked.connect(self.tempUP5_2)
        self.bUP6_2.clicked.connect(self.tempUP6_2)
        self.bUP7_2.clicked.connect(self.tempUP7_2)

        self.bUP_3.clicked.connect(self.tempUP_3)
        self.bUP2_3.clicked.connect(self.tempUP2_3)
        self.bUP3_3.clicked.connect(self.tempUP3_3)
        self.bUP4_3.clicked.connect(self.tempUP4_3)
        self.bUP5_3.clicked.connect(self.tempUP5_3)
        self.bUP6_3.clicked.connect(self.tempUP6_3)
        self.bUP7_3.clicked.connect(self.tempUP7_3)

        self.bDOWN.clicked.connect(self.tempDOWN)
        self.bDOWN2.clicked.connect(self.tempDOWN2)
        self.bDOWN3.clicked.connect(self.tempDOWN3)
        self.bDOWN4.clicked.connect(self.tempDOWN4)
        self.bDOWN5.clicked.connect(self.tempDOWN5)
        self.bDOWN6.clicked.connect(self.tempDOWN6)
        self.bDOWN7.clicked.connect(self.tempDOWN7)

        self.bDOWN_2.clicked.connect(self.tempDOWN_2)
        self.bDOWN2_2.clicked.connect(self.tempDOWN2_2)
        self.bDOWN3_2.clicked.connect(self.tempDOWN3_2)
        self.bDOWN4_2.clicked.connect(self.tempDOWN4_2)
        self.bDOWN5_2.clicked.connect(self.tempDOWN5_2)
        self.bDOWN6_2.clicked.connect(self.tempDOWN6_2)
        self.bDOWN7_2.clicked.connect(self.tempDOWN7_2)

        self.bDOWN_3.clicked.connect(self.tempDOWN_3)
        self.bDOWN2_3.clicked.connect(self.tempDOWN2_3)
        self.bDOWN3_3.clicked.connect(self.tempDOWN3_3)
        self.bDOWN4_3.clicked.connect(self.tempDOWN4_3)
        self.bDOWN5_3.clicked.connect(self.tempDOWN5_3)
        self.bDOWN6_3.clicked.connect(self.tempDOWN6_3)
        self.bDOWN7_3.clicked.connect(self.tempDOWN7_3)

        self.reset.clicked.connect(self.Reset)
        self.reset2.clicked.connect(self.Reset2)
        self.reset3.clicked.connect(self.Reset3)
        self.reset4.clicked.connect(self.Reset4)
        self.reset5.clicked.connect(self.Reset5)
        self.reset6.clicked.connect(self.Reset6)
        self.reset7.clicked.connect(self.Reset7)

        self.reset_2.clicked.connect(self.Reset_2)
        self.reset2_2.clicked.connect(self.Reset2_2)
        self.reset3_2.clicked.connect(self.Reset3_2)
        self.reset4_2.clicked.connect(self.Reset4_2)
        self.reset5_2.clicked.connect(self.Reset5_2)
        self.reset6_2.clicked.connect(self.Reset6_2)
        self.reset7_2.clicked.connect(self.Reset7_2)

        self.reset_3.clicked.connect(self.Reset_3)
        self.reset2_3.clicked.connect(self.Reset2_3)
        self.reset3_3.clicked.connect(self.Reset3_3)
        self.reset4_3.clicked.connect(self.Reset4_3)
        self.reset5_3.clicked.connect(self.Reset5_3)
        self.reset6_3.clicked.connect(self.Reset6_3)
        self.reset7_3.clicked.connect(self.Reset7_3)

        self.loadJson()

    def tempUP(self):
        self.save.setEnabled(True)
        for item in self.table.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP2(self):
        self.save.setEnabled(True)
        for item in self.table2.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP3(self):
        self.save.setEnabled(True)
        for item in self.table3.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP4(self):
        self.save.setEnabled(True)
        for item in self.table4.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP5(self):
        self.save.setEnabled(True)
        for item in self.table5.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP6(self):
        self.save.setEnabled(True)
        for item in self.table6.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP7(self):
        self.save.setEnabled(True)
        for item in self.table7.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP_2(self):
        self.save.setEnabled(True)
        for item in self.table_2.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP2_2(self):
        self.save.setEnabled(True)
        for item in self.table2_2.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP3_2(self):
        self.save.setEnabled(True)
        for item in self.table3_2.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP4_2(self):
        self.save.setEnabled(True)
        for item in self.table4_2.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP5_2(self):
        self.save.setEnabled(True)
        for item in self.table5_2.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP6_2(self):
        self.save.setEnabled(True)
        for item in self.table6_2.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP7_2(self):
        self.save.setEnabled(True)
        for item in self.table7_2.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP_3(self):
        self.save.setEnabled(True)
        for item in self.table_3.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP2_3(self):
        self.save.setEnabled(True)
        for item in self.table2_3.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP3_3(self):
        self.save.setEnabled(True)
        for item in self.table3_3.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP4_3(self):
        self.save.setEnabled(True)
        for item in self.table4_3.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP5_3(self):
        self.save.setEnabled(True)
        for item in self.table5_3.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP6_3(self):
        self.save.setEnabled(True)
        for item in self.table6_3.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempUP7_3(self):
        self.save.setEnabled(True)
        for item in self.table7_3.selectedItems():
            item.setText(str(float(item.text()) + 0.5))

    def tempDOWN(self):
        self.save.setEnabled(True)
        for item in self.table.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN2(self):
        self.save.setEnabled(True)
        for item in self.table2.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN3(self):
        self.save.setEnabled(True)
        for item in self.table3.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN4(self):
        self.save.setEnabled(True)
        for item in self.table4.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN5(self):
        self.save.setEnabled(True)
        for item in self.table5.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN6(self):
        self.save.setEnabled(True)
        for item in self.table6.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN7(self):
        self.save.setEnabled(True)
        for item in self.table7.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN_2(self):
        self.save.setEnabled(True)
        for item in self.table_2.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN2_2(self):
        self.save.setEnabled(True)
        for item in self.table2_2.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN3_2(self):
        self.save.setEnabled(True)
        for item in self.table3_2.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN4_2(self):
        self.save.setEnabled(True)
        for item in self.table4_2.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN5_2(self):
        self.save.setEnabled(True)
        for item in self.table5_2.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN6_2(self):
        self.save.setEnabled(True)
        for item in self.table6_2.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN7_2(self):
        self.save.setEnabled(True)
        for item in self.table7_2.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN_3(self):
        self.save.setEnabled(True)
        for item in self.table_3.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN2_3(self):
        self.save.setEnabled(True)
        for item in self.table2_3.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN3_3(self):
        self.save.setEnabled(True)
        for item in self.table3_3.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN4_3(self):
        self.save.setEnabled(True)
        for item in self.table4_3.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN5_3(self):
        self.save.setEnabled(True)
        for item in self.table5_3.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN6_3(self):
        self.save.setEnabled(True)
        for item in self.table6_3.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def tempDOWN7_3(self):
        self.save.setEnabled(True)
        for item in self.table7_3.selectedItems():
            item.setText(str(float(item.text()) - 0.5))

    def Reset(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table.item(day, hour).setText('20.0')

    def Reset2(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table2.item(day, hour).setText('20.0')

    def Reset3(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table3.item(day, hour).setText('20.0')

    def Reset4(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table4.item(day, hour).setText('20.0')

    def Reset5(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table5.item(day, hour).setText('20.0')

    def Reset6(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table6.item(day, hour).setText('20.0')

    def Reset7(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table7.item(day, hour).setText('20.0')

    def Reset_2(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table_2.item(day, hour).setText('20.0')

    def Reset2_2(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table2_2.item(day, hour).setText('20.0')

    def Reset3_2(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table3_2.item(day, hour).setText('20.0')

    def Reset4_2(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table4_2.item(day, hour).setText('20.0')

    def Reset5_2(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table5_2.item(day, hour).setText('20.0')

    def Reset6_2(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table6_2.item(day, hour).setText('20.0')

    def Reset7_2(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table7_2.item(day, hour).setText('20.0')

    def Reset_3(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table_3.item(day, hour).setText('20.0')

    def Reset2_3(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table2_3.item(day, hour).setText('20.0')

    def Reset3_3(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table3_3.item(day, hour).setText('20.0')

    def Reset4_3(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table4_3.item(day, hour).setText('20.0')

    def Reset5_3(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table5_3.item(day, hour).setText('20.0')

    def Reset6_3(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table6_3.item(day, hour).setText('20.0')

    def Reset7_3(self):
        self.save.setEnabled(True)
        for day in range(2):
            for hour in range(12):
                self.table7_3.item(day, hour).setText('20.0')

    def closeW(self):
        self.close()
        self.w.setEnabled(True)

    def loadJson(self):
        f = open('schedule_living.json', 'r')
        obj = json.loads(f.read())
        idx = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun'}
        tables = [self.table, self.table2, self.table3, self.table4, self.table5, self.table6, self.table7]
        for day, t in enumerate(tables, 1):
            for hour in range(24):
                t.item(hour / 12, hour % 12).setText(obj[idx[day]][hour])
        f.close()

        f = open('schedule_kitchen.json', 'r')
        obj = json.loads(f.read())
        idx = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun'}
        tables = [self.table_2, self.table2_2, self.table3_2, self.table4_2, self.table5_2, self.table6_2, self.table7_2]
        for day, t in enumerate(tables, 1):
            for hour in range(24):
                t.item(hour / 12, hour % 12).setText(obj[idx[day]][hour])
        f.close()

        f = open('schedule_bedroom.json', 'r')
        obj = json.loads(f.read())
        idx = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun'}
        tables = [self.table_3, self.table2_3, self.table3_3, self.table4_3, self.table5_3, self.table6_3, self.table7_3]
        for day, t in enumerate(tables, 1):
            for hour in range(24):
                t.item(hour / 12, hour % 12).setText(obj[idx[day]][hour])
        f.close()

    def writeJson(self):
        timer = QtCore.QTimer(self)
        self.save.setEnabled(False)
        self.Saved.setVisible(True)
        timer.setInterval(2000)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.Saved.setVisible(False))
        timer.start()

        f = open('schedule_living.json', 'w')
        obj = {'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': [], 'Sat': [], 'Sun': []}
        idx = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun'}
        i = 1
        tables = [self.table, self.table2, self.table3, self.table4, self.table5, self.table6, self.table7]
        for t in tables:
            for row in range(t.rowCount()):
                for column in range(t.columnCount()):
                    item = t.item(row, column)
                    obj[idx[i]].append(item.text())
            i = i+1
        f.write(json.dumps(obj, indent=2))
        f.close()

        f = open('schedule_kitchen.json', 'w')
        obj = {'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': [], 'Sat': [], 'Sun': []}
        idx = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun'}
        i = 1
        tables = [self.table_2, self.table2_2, self.table3_2, self.table4_2, self.table5_2, self.table6_2, self.table7_2]
        for t in tables:
            for row in range(t.rowCount()):
                for column in range(t.columnCount()):
                    item = t.item(row, column)
                    obj[idx[i]].append(item.text())
            i = i + 1
        f.write(json.dumps(obj, indent=2))
        f.close()

        f = open('schedule_bedroom.json', 'w')
        obj = {'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': [], 'Sat': [], 'Sun': []}
        idx = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun'}
        i = 1
        tables = [self.table_3, self.table2_3, self.table3_3, self.table4_3, self.table5_3, self.table6_3, self.table7_3]
        for t in tables:
            for row in range(t.rowCount()):
                for column in range(t.columnCount()):
                    item = t.item(row, column)
                    obj[idx[i]].append(item.text())
            i = i + 1
        f.write(json.dumps(obj, indent=2))
        f.close()
