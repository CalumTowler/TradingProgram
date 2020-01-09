import os
import sys
from MainApp         import App
from PyQt5.QtGui     import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen, QProgressBar

def main(sys):
    app = QApplication(sys.argv)
    show_splash = True
    for token in sys.argv:
        if token == '-nosplash' or token == '--nosplash':
            show_splash = False
        elif token == '-h' or token == '-help' or token == '--help':
            print('TEST - Help Function')
            exit()

    if show_splash:
        # Starting picture
        dirname = os.path.dirname(os.path.realpath(sys.argv[0]))
        splashfile = os.path.join(dirname, 'middlefinger.png')
        pixmap = QPixmap(splashfile)
        splash = QSplashScreen(pixmap)
        progressbar = QProgressBar(splash)
        splash.show()
    else:
        progressbar = QProgressBar()
        progressbar = None
    ex = App(sys.argv, progressbar)
    ex.show()
    if show_splash:
        splash.finish(ex)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys)