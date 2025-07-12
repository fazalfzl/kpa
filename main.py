import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

from ui.main.pos_main_controller import POSMainController


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # 🖼️ Setup splash screen
    splash_pix = QPixmap("assets/splash.png")  # ✅ Replace with your actual splash image path
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    splash.show()
    app.processEvents()

    # 🕐 Simulate loading process or load the heavy logic here if needed
    def start_main_window():
        window = POSMainController()
        window.show()
        splash.finish(window)  # Hide splash when window is ready

    # ⏱️ Delay starting main window (adjust time or use real loading logic)
    QTimer.singleShot(2000, start_main_window)  # 2000 ms = 2 seconds

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
