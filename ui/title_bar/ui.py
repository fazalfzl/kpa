# custom_title_bar_ui.py

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel, QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

from utils.constants import *
from ui.utils.styles import TitleBarStyles, CategoryButtonStyles, BarcodeInputStyles, TitleLabelStyles


class CustomTitleBar(QWidget):
    show_category = pyqtSignal(str)
    barcode_scanned = pyqtSignal(str)
    load_bill = pyqtSignal(int)

    def __init__(self, logic, parent=None):
        super().__init__(parent)
        self.logic = logic
        self.parent = parent
        self.last_bill_buttons = []

        self._drag_pos = QPoint()
        self.pressing = False

        self._build_ui()
        self.logic.connect_signals(self)

    def _build_ui(self):
        self.setFixedHeight(TITLE_BAR_HEIGHT)
        self.setStyleSheet(TitleBarStyles.TITLE_BAR_STYLE)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(TITLE_BAR_MARGIN, 0, TITLE_BAR_MARGIN, 0)
        layout.setSpacing(TITLE_BAR_SPACING)

        layout.addLayout(self._create_left())
        layout.addLayout(self._create_middle())
        layout.addStretch()
        layout.addLayout(self._create_right())

        self.setLayout(layout)

    def _create_left(self):
        layout = QHBoxLayout()
        layout.setSpacing(TITLE_BAR_LEFT_SPACING)

        self.menu_btn = QPushButton("☰")
        self.menu_btn.setFixedSize(MENU_BUTTON_SIZE, MENU_BUTTON_SIZE)
        self.menu_btn.setFont(QFont(TITLE_BAR_FONT_FAMILY, MENU_BUTTON_FONT_SIZE))
        self.menu_btn.setStyleSheet(TitleBarStyles.MENU_BUTTON_STYLE)
        self.menu_btn.clicked.connect(self.logic.show_menu)
        layout.addWidget(self.menu_btn)

        self.title_label = QLabel(APP_TITLE)
        self.title_label.setFont(QFont(TITLE_BAR_FONT_FAMILY, TITLE_BAR_FONT_SIZE, QFont.Bold))
        self.title_label.setStyleSheet(TitleLabelStyles.LABEL_STYLE)
        layout.addWidget(self.title_label)

        return layout

    def _create_middle(self):
        layout = QHBoxLayout()
        layout.setSpacing(TITLE_BAR_SPACING)

        self.fruits_btn = QPushButton("🍏 Fruits & Veg")
        self.fruits_btn.setFixedSize(FRUITS_BUTTON_WIDTH, FRUITS_BUTTON_HEIGHT)
        self.fruits_btn.setStyleSheet(CategoryButtonStyles.FRUITS_BUTTON_STYLE)
        self.fruits_btn.clicked.connect(lambda: self.show_category.emit("fruits_veg"))
        layout.addWidget(self.fruits_btn)

        self.manual_btn = QPushButton("📦 Manual")
        self.manual_btn.setFixedSize(MANUAL_BUTTON_WIDTH, MANUAL_BUTTON_HEIGHT)
        self.manual_btn.setStyleSheet(CategoryButtonStyles.MANUAL_BUTTON_STYLE)
        self.manual_btn.clicked.connect(lambda: self.show_category.emit("manual"))
        layout.addWidget(self.manual_btn)

        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText(BARCODE_PLACEHOLDER)
        self.barcode_input.setFixedSize(BARCODE_INPUT_WIDTH, BARCODE_INPUT_HEIGHT)
        self.barcode_input.setStyleSheet(BarcodeInputStyles.INPUT_STYLE)
        self.barcode_input.returnPressed.connect(self.logic.on_barcode_entered)
        layout.addWidget(self.barcode_input)

        self.logic.add_last_bill_buttons(layout)

        self.bill_input = QLineEdit()
        self.bill_input.setPlaceholderText("ID")
        self.bill_input.setFixedSize(80, 30)  # Smaller width and height
        self.bill_input.setStyleSheet(BarcodeInputStyles.INPUT_STYLE)
        self.bill_input.returnPressed.connect(self.logic.on_load_bill)
        # layout.addWidget(self.bill_input)

        self.load_bill_icon = QPushButton("📄")  # You can also use an icon via QIcon
        self.load_bill_icon.setFixedSize(30, 30)
        self.load_bill_icon.setFont(QFont(TITLE_BAR_FONT_FAMILY, 10))  # Small font for emoji
        self.load_bill_icon.setStyleSheet(TitleBarStyles.MENU_BUTTON_STYLE)
        self.load_bill_icon.clicked.connect(self.logic.on_load_bill)
        # layout.addWidget(self.load_bill_icon)


        return layout

    def _create_right(self):
        layout = QHBoxLayout()
        layout.setSpacing(5)

        self.minimize_btn = QPushButton("−")
        self.minimize_btn.setFixedSize(WINDOW_CONTROL_BUTTON_SIZE, WINDOW_CONTROL_BUTTON_SIZE)
        self.minimize_btn.setFont(QFont(TITLE_BAR_FONT_FAMILY, WINDOW_CONTROL_FONT_SIZE, QFont.Bold))
        self.minimize_btn.setStyleSheet(TitleBarStyles.MINIMIZE_BUTTON_STYLE)
        self.minimize_btn.clicked.connect(self.logic.minimize_window)
        layout.addWidget(self.minimize_btn)

        self.maximize_btn = QPushButton("□")
        self.maximize_btn.setFixedSize(WINDOW_CONTROL_BUTTON_SIZE, WINDOW_CONTROL_BUTTON_SIZE)
        self.maximize_btn.setFont(QFont(TITLE_BAR_FONT_FAMILY, MAXIMIZE_BUTTON_FONT_SIZE, QFont.Bold))
        self.maximize_btn.setStyleSheet(TitleBarStyles.MAXIMIZE_BUTTON_STYLE)
        self.maximize_btn.clicked.connect(self.logic.toggle_maximize)
        layout.addWidget(self.maximize_btn)

        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(WINDOW_CONTROL_BUTTON_SIZE, WINDOW_CONTROL_BUTTON_SIZE)
        self.close_btn.setFont(QFont(TITLE_BAR_FONT_FAMILY, WINDOW_CONTROL_FONT_SIZE, QFont.Bold))
        self.close_btn.setStyleSheet(TitleBarStyles.CLOSE_BUTTON_STYLE)
        self.close_btn.clicked.connect(self.logic.close_application)
        layout.addWidget(self.close_btn)

        return layout

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = self.mapToGlobal(event.pos())
            self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing and self.parent:
            end = self.mapToGlobal(event.pos())
            movement = end - self._drag_pos
            self.parent.setGeometry(
                self.mapToGlobal(movement).x(), self.mapToGlobal(movement).y(),
                self.parent.width(), self.parent.height()
            )
            self._drag_pos = end

    def mouseReleaseEvent(self, event):
        self.pressing = False
