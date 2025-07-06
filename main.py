import sys
from PyQt5.QtWidgets import QApplication

from ui.pos.pos_window import POSWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = POSWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()