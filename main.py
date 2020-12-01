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
        self.pushButton.clicked.connect(self.open_CreateItemForm)

    def load_table(self):
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

    def open_CreateItemForm(self):
        form = CreateItemForm(self)
        form.show()

    def add_item(self, sort, roast, ground_type, description, cost, volume):
        req = """
              INSERT INTO genres (sort, roast, ground_type, description, cost, volume)
              VALUES(?, ?, ?, ?, ?, ?)
              """

        self.con.execute(req, (sort, roast, ground_type, description, cost, volume))
        self.con.commit()
        self.load_table()


class CreateItemForm(QMainWindow):
    def __init__(self, parent=None):
        super(CreateItemForm, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui')
        self.pushButton.clicked.connect(self.save_item)

    def save_item(self):
        sort = self.lineEdit.text()
        roast = self.lineEdit.text_2()
        # ground_type = self.checkBox
        ground_type = True
        description = self.lineEdit.text_4()
        cost = self.lineEdit.text_5()
        volume = self.lineEdit.text_6()

        self.parent().add_item(sort, roast, ground_type, description, cost, volume)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())