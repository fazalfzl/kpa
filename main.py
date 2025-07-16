import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Show splash first
    splash_pix = QPixmap("assets/splash.png")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    # splash.show()
    app.processEvents()

    # Delayed function to load the heavy window
    def start_main_window():
        # ⏬ DEFERRED IMPORT of heavy controller
        from ui.main.pos_main_controller import POSMainController

        window = POSMainController()
        window.show()
        splash.finish(window)

    # ⏱ Start loading after slight delay to ensure splash appears
    QTimer.singleShot(100, start_main_window)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
