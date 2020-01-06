import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args,**kwargs,)

        self.setWindowTitle('My Awesome App')

        label = QLabel('This is a PyQt5 Window!')

        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

class CustomButton(QPushButton):

    def keyPressEvent(self, e):
        super(CustomButton, self).keyPressEvent(e)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()