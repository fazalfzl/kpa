from PyQt5.QtWidgets import QMessageBox
from core.services.product_service import ProductService


class POSEventHandler:
    def __init__(self, billing_list):
        self.billing_list = billing_list
        self.service = ProductService()

    def handle_product_click(self, product):
        if product:
            self.billing_list.add_item(name=product.name, qty=1, price=product.price)

    def handle_barcode(self, barcode):
        try:
            product = self.service.get_by_barcode(barcode)
            if product:
                self.billing_list.add_item(product.name, 1, product.price)
            else:
                QMessageBox.warning(None, "Not Found", f"No product for barcode: {barcode}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Barcode error: {e}")
