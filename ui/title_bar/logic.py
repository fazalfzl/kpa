# custom_title_bar_logic.py

from PyQt5.QtWidgets import QMessageBox, QPushButton, QMenu, QAction, QDialog
from PyQt5.QtCore import QPoint
from core.services.bill_service import BillService
from ui.product.editor import ProductEditorDialog
from ui.product.manager_dialog import ProductManagementDialog
from ui.product.order_dialog import OrderProductsDialog
from utils.print_pkg.printer_config import PrinterTester
from ui.utils.styles import TitleBarStyles

from utils.logger import get_logger
log = get_logger(__name__)


class CustomTitleBarLogic:
    def __init__(self, parent=None):
        self.parent = parent
        self.bill_service = BillService()
        self.last_bill_buttons = []
        self.ui = None

    def connect_signals(self, ui):
        self.ui = ui

    def on_load_bill(self):
        bill_id = self.ui.bill_input.text().strip()
        if bill_id.isdigit():
            self.ui.load_bill.emit(int(bill_id))
            self.ui.bill_input.clear()
        else:
            QMessageBox.warning(self.ui, "Invalid Input", "Please enter a valid bill ID.")

    def add_last_bill_buttons(self, layout):
        self.last_bill_buttons.clear()
        for _ in range(3):
            btn = QPushButton()
            btn.setFixedSize(120, 40)
            btn.setStyleSheet(TitleBarStyles.LAST_BILL_BUTTON_STYLE)
            btn.clicked.connect(self._on_last_bill_clicked)
            self.last_bill_buttons.append(btn)
            layout.addWidget(btn)
        self.refresh_last_bills()

    def refresh_last_bills(self):
        bills = self.bill_service.list_bills()[:3]
        for i, btn in enumerate(self.last_bill_buttons):
            if i < len(bills):
                bill = bills[i]
                btn.setText(f"Bill {bill.id}\n₹{bill.total:.2f}")
                btn.setProperty("bill_id", bill.id)
                btn.setEnabled(True)
            else:
                btn.setText("No Bill")
                btn.setEnabled(False)

    def _on_last_bill_clicked(self):
        bill_id = self.ui.sender().property("bill_id")
        if bill_id:
            self.ui.load_bill.emit(bill_id)

    def on_barcode_entered(self):
        barcode = self.ui.barcode_input.text().strip()
        if barcode:
            self.ui.barcode_scanned.emit(barcode)
            self.ui.barcode_input.clear()

    def show_menu(self):
        menu = QMenu(self.ui)
        menu.setStyleSheet(TitleBarStyles.MENU_STYLE)

        items = [
            ("➕ Create Product", self._open_create_product),
            ("↕️ Order Products", self._open_order_products),
            ("🛠️ Manage Products", self._open_product_management),
            ("📁 File", lambda: log.info("File clicked")),
            ("⚙️ Settings", lambda: log.info("Settings clicked")),
            ("📊 Reports", lambda: log.info("Reports clicked")),
            ("📦 Inventory", lambda: log.info("Inventory clicked")),
            ("❓ Help", lambda: log.info("Help clicked")),
            ("ℹ️ About", lambda: log.info("About clicked")),
            ("🖨️ Test Printer", self._test_printer)
        ]

        for text, func in items:
            if "File" in text or "Settings" in text:
                menu.addSeparator()
            action = QAction(text, self.ui)
            action.triggered.connect(func)
            menu.addAction(action)

        pos = self.ui.menu_btn.mapToGlobal(QPoint(0, self.ui.menu_btn.height()))
        menu.exec_(pos)

    def _test_printer(self):
        tester = PrinterTester()
        tester.run()
        tester.test_printer()

    def _open_product_management(self):
        ProductManagementDialog(self.parent).exec_()

    def _open_create_product(self):
        dlg = ProductEditorDialog(self.parent)
        if dlg.exec_() == QDialog.Accepted:
            self.parent.main_content.products_sec.refresh()

    def _open_order_products(self):
        dlg = OrderProductsDialog(self.parent)
        if dlg.exec_() == QDialog.Accepted:
            self.parent.main_content.products_sec.refresh()

    def minimize_window(self):
        if self.parent:
            self.parent.showMinimized()

    def toggle_maximize(self):
        if self.parent:
            if self.parent.isMaximized():
                self.parent.showNormal()
                self.ui.maximize_btn.setText("□")
            else:
                self.parent.showMaximized()
                self.ui.maximize_btn.setText("❐")

    def close_application(self):
        if self.parent:
            self.parent.close()
