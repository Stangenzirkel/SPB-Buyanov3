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
        self.pushButton_2.clicked.connect(self.open_EditItemForm)
        self.tableWidget.itemSelectionChanged.connect(self.item_clicked)
        self.tableWidget.item(0, 0).setSelected(True)

    def load_table(self):
        result = list(self.con.execute('SELECT * FROM coffee'))
        if result is None:
            return None

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setHorizontalHeaderLabels(['id',
                                                    'сорт',
                                                    'степень обжарки',
                                                    'молотый',
                                                    'описание',
                                                    'цена',
                                                    'объем'])

        for i, elem in enumerate(result):
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

    def item_clicked(self):
        for i in range(7):
            self.tableWidget.item(self.sender().selectedItems()[0].row(), i).setSelected(True)
        self.current_selection = self.sender().selectedItems()[0].row()

    def open_CreateItemForm(self):
        form = CreateItemForm(self)
        form.show()

    def open_EditItemForm(self):
        id = self.tableWidget.item(self.current_selection, 0).text()
        form = EditItemForm(id, self)
        form.show()

    def add_item(self, sort, roast, ground_type, description, cost, volume):
        req = """
              INSERT INTO coffee (sort, roast, ground_type, description, cost, volume)
              VALUES(?, ?, ?, ?, ?, ?)
              """

        self.con.execute(req, (sort, roast, ground_type, description, cost, volume))
        self.con.commit()
        self.load_table()

    def edit_item(self, id, sort, roast, ground_type, description, cost, volume):
        req = """
              UPDATE coffee 
              SET sort = ?, roast = ?, ground_type = ?, description = ?, cost = ?, volume = ?
              WHERE id = ?
              """

        self.con.execute(req, (sort, roast, ground_type, description, cost, volume, id))
        self.con.commit()
        self.load_table()


class CreateItemForm(QMainWindow):
    def __init__(self, parent=None):
        super(CreateItemForm, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.save_item)

    def save_item(self):
        sort = self.lineEdit.text()
        roast = self.lineEdit_2.text()
        ground_type = self.checkBox.isChecked()
        description = self.lineEdit_4.text()
        cost = self.lineEdit_5.text()
        volume = self.lineEdit_6.text()

        self.parent().add_item(sort, roast, ground_type, description, cost, volume)
        self.close()


class EditItemForm(QMainWindow):
    def __init__(self, id, parent=None):
        self.id = id
        super(EditItemForm, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.save_item)
        self.load_info()

    def load_info(self):
        result = list(self.parent().con.execute('SELECT * FROM coffee WHERE id = ?', (self.id,)))[0]
        result = list(map(str, result))

        self.lineEdit.setText(result[1])
        self.lineEdit_2.setText(result[2])
        self.lineEdit_4.setText(result[4])
        self.lineEdit_5.setText(result[5])
        self.lineEdit_6.setText(result[6])
        self.checkBox.setCheckState(result[3] == '1')
        self.checkBox.setTristate(False)

    def save_item(self):
        sort = self.lineEdit.text()
        roast = self.lineEdit_2.text()
        ground_type = self.checkBox.isChecked()
        description = self.lineEdit_4.text()
        cost = self.lineEdit_5.text()
        volume = self.lineEdit_6.text()

        self.parent().edit_item(self.id, sort, roast, ground_type, description, cost, volume)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())