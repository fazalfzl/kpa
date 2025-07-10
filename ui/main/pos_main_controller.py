# 📁 ui/main/pos_main_controller.py

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from core.services.product_service import ProductService
from ui.main.pos_main_ui import POSMainUI
from ui.title_bar.logic import CustomTitleBarLogic
from ui.main.pos_event_handler import POSEventHandler
from utils.constants import DEFAULT_CATEGORY
from utils.weight import weight_manager

class POSMainController(POSMainUI):
    def __init__(self):
        self.title_bar_logic = CustomTitleBarLogic(self)
        super().__init__(self.title_bar_logic)
        self.product_service = ProductService()
        self.event_handler = POSEventHandler(self.billing_section.billing_list)

        self._connect_signals()
        weight_manager.start()

        self.action_barcode_input = self.billing_section.action_buttons_ui.barcode_input
        self.action_barcode_input.returnPressed.connect(self._handle_barcode_input)

    def _handle_barcode_input(self):
        barcode = self.action_barcode_input.text().strip()
        if barcode:
            self.event_handler.handle_barcode(barcode)
            self.action_barcode_input.clear()

    def _connect_signals(self):
        products_sec = self.main_content.products_sec

        products_sec.on_product_click = self.event_handler.handle_product_click
        self.title_bar.show_category.connect(self._on_category_changed)
        self.title_bar.load_bill.connect(self.billing_section.load_bill)

        products_sec.set_category(DEFAULT_CATEGORY)

    def _on_category_changed(self, category):
        self.main_content.products_sec.set_category(category)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)
