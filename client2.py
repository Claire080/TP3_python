import webbrowser as wb

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(400, 400)

        self.label_0= QLabel("Enter your host IP:", self)
        self.text_0 = QLineEdit(self)
        self.text_0.move(10, 30)

        self.label_1 = QLabel("Enter your API Key:", self)
        self.label_1.move(0, 70)
        self.text_1 = QLineEdit(self)
        self.text_1.move(10, 100)

        self.label_2 = QLabel("Enter the hostname:", self)
        self.label_2.move(0, 140)
        self.text_2 = QLineEdit(self)
        self.text_2.move(10, 170)

        self.label2 = QLabel("Answer:", self)
        self.label2.move(10, 240)

        self.button = QPushButton("Send", self)
        self.button.move(10, 270)

        self.button.clicked.connect(self.on_click)
        self.button.pressed.connect(self.on_click)

        self.show()

    def on_click(self):
        host = self.text_0.text()
        api=self.text_1.text()
        hostname=self.text_2.text()

        if hostname == "":
            QMessageBox.about(self, "Error", "Please fill the field")
        else:
            res = self.__query(hostname,host,api)
            if res:
                self.label2.setText("Answer %s %s" % (res["Latitude"],res["Longitude"]))
                self.label2.adjustSize()
                self.show()
                url2 = "http://www.openstreetmap.org/?mlat=%s&mlon=%s#map=12" % (res["Latitude"],res["Longitude"])
                wb.open_new_tab(url2)




    def __query(self, hostname,host,api):
        #url = "http://%s" % (hostname)
        url = "http://%s/ip/%s?key=%s" % (hostname,host,api)
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found")
        if r.status_code == requests.codes.OK:
            return r.json()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()