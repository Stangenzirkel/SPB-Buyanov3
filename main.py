import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5 import uic


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('coffee.sqlite')
        uic.loadUi('main.ui', self)
        self.load_table()

    def load_table(self):
        cur = self.con.cursor()

        result = self.con.execute('SELECT * FROM coffee')
        if result is None:
            return None

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['id',
                                                    'сорт',
                                                    'степень обжарки',
                                                    'молотый',
                                                    'описание',
                                                    'цена',
                                                    'объем'])

        for i, elem in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

        self.tableWidget.setColumnWidth(0, 30)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 110)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setColumnWidth(4, 308)
        self.tableWidget.setColumnWidth(5, 50)
        self.tableWidget.setColumnWidth(6, 50)
        self.tableWidget.verticalHeader().hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())