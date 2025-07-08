# pos_main_window.py

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from ui.pos_main_ui import POSMainUI
from ui.custom_title_bar_logic import CustomTitleBarLogic
from database.product_repository import ProductRepository
from utils.constants import DEFAULT_CATEGORY

class POSMainController(POSMainUI):
    def __init__(self):
        self.title_bar_logic = CustomTitleBarLogic(self)
        super().__init__(self.title_bar_logic)
        self.product_dao = ProductRepository()

        self._connect_signals()

    def _connect_signals(self):
        products_sec = self.main_content.products_sec
        billing_list = self.billing_section.billing_list
        products_sec.on_product_click = lambda p: billing_list.add_item(name=p.name, qty=1, price=p.price)

        self.title_bar.show_category.connect(self._on_category_changed)
        self.title_bar.barcode_scanned.connect(self._on_barcode_scanned)
        self.title_bar.load_bill.connect(self.billing_section.load_bill)

        products_sec.set_category(DEFAULT_CATEGORY)

    def _on_category_changed(self, category):
        self.main_content.products_sec.set_category(category)

    def _on_barcode_scanned(self, barcode):
        try:
            product = self.product_dao.get_by_barcode(barcode)
            if product:
                self.billing_section.billing_list.add_item(product.name, 1, product.price)
            else:
                QMessageBox.warning(self, "Not Found", f"No product for barcode: {barcode}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Barcode error: {e}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)
