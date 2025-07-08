import sys
from PyQt5.QtWidgets import QApplication
from ui.pos_main_window import POSMainController  # 🆕 import the controller


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = POSMainController()  # 🆕 use controller instead of POSWindow
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
