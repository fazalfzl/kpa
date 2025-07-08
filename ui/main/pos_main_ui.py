# pos_main_ui.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

from ui.billing.section.logic import BillingSection
from ui.product.main_area import MainContent
from ui.title_bar.ui import CustomTitleBar

from ui.utils.styles import GlobalStyles
from utils.constants import BILLING_SECTION_WIDTH

class POSMainUI(QWidget):
    def __init__(self, title_bar_logic, parent=None):
        super().__init__(parent)
        self.title_bar = CustomTitleBar(logic=title_bar_logic, parent=self)
        self.main_content = MainContent()
        self.billing_section = BillingSection(title_bar_logic=title_bar_logic)

        self._setup_ui()
        self.billing_section.action_buttons_ui.title_bar = self.title_bar

    def _setup_ui(self):
        self.setWindowTitle("My POS System")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.title_bar)

        content_layout = QHBoxLayout()
        content_widget = QWidget()
        content_widget.setLayout(content_layout)

        left = self.main_content.create_main_content_area()
        content_layout.addWidget(left, 3)

        right = self.billing_section.create_billing_section()
        right.setFixedWidth(BILLING_SECTION_WIDTH)
        content_layout.addWidget(right, 1)

        main_layout.addWidget(content_widget)
        self.setStyleSheet(GlobalStyles.GLOBAL_STYLE)
