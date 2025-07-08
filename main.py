import sys
from PyQt5.QtWidgets import QApplication

from ui.main.pos_main_controller import POSMainController


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = POSMainController()  # 🆕 use controller instead of POSWindow
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
