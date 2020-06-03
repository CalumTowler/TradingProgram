import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QCoreApplication
# from Python.GUI.NoteBook import NoteBook


class App(QMainWindow):

    def __init__(self, args, progressbar):
        super().__init__()
        exit = False
        # Manage options
        tokens = args[1:]
        ntokens = len(tokens)
        itoken = 0
        while itoken < ntokens:
            token = tokens[itoken]
            if token == '-nosplash' or token == '--nosplash':
                nosplash = True
            elif token == '-exit' or token == '--exit' or token == '-quit' or token == '--quit':
                exit = True
            elif token == '-h' or token == '-help' or token == '--help':
                print('TEST - Help Message')
                exit()
            itoken += 1
        #
        self.title = 'Oracle GUI'
        self.left = 200
        self.top = 100
        self.width = 1500
        self.height = 900
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        QCoreApplication.processEvents()
        if exit:
            sys.exit()
        self.show()

    def readScript(self, scriptname):
        print('Test Function 1')
        QCoreApplication.processEvents()

    def closeEvent(self, event):
        super(App, self).closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(sys.argv)
    ex.show()
    sys.exit(app.exec_())