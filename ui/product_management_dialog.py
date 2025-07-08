from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTabWidget, QWidget, QToolButton,
    QPushButton, QHBoxLayout, QMessageBox, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap
from ui.edit_product_dialog import ProductEditorDialog
from database.product_repository import ProductRepository
import os

from ui.utils.styles import GlobalStyles


IMAGE_DIR = os.path.join(os.getcwd(), "product_images")
PRODUCT_ICON_SIZE = 128
PRODUCT_GRID_COLUMNS = 3


class ProductManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Product Management")
        self.dao = ProductRepository()
        self.tabs = {}
        self.selected_btn = None
        self.selected_product = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.tab_widget = QTabWidget()
        for category in ["fruits_veg", "manual", "barcode_only"]:
            self.tabs[category] = self._create_product_grid(category)
            self.tab_widget.addTab(self.tabs[category]["widget"], category.replace("_", " ").title())
        layout.addWidget(self.tab_widget)

        # Control Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Product")
        self.add_btn.clicked.connect(self._add_product)
        self.edit_btn = QPushButton("Edit Product")
        self.edit_btn.clicked.connect(self._edit_product)
        self.delete_btn = QPushButton("Delete Product")
        self.delete_btn.clicked.connect(self._delete_product)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)

    def _create_product_grid(self, category):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        grid = QGridLayout(content_widget)
        scroll_area.setWidget(content_widget)

        return {
            "widget": scroll_area,
            "grid": grid,
            "category": category,
            "buttons": [],
            "content_widget": content_widget,
        }

    def _load_grid(self, tab):
        # Clear old buttons
        layout = tab["grid"]
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()
        tab["buttons"] = []
        tab["selected_btn"] = None

        # Load new buttons
        products = self.dao.get_by_category(tab["category"])
        for i, product in enumerate(products):
            btn = self._make_product_button(product)
            layout.addWidget(btn, i // PRODUCT_GRID_COLUMNS, i % PRODUCT_GRID_COLUMNS)
            tab["buttons"].append((btn, product))

    def _make_product_button(self, product):
        btn = QToolButton()
        btn.setFixedSize(160, 160)
        btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn.setIcon(self._get_icon(product.image_path))
        btn.setIconSize(QSize(PRODUCT_ICON_SIZE, PRODUCT_ICON_SIZE))
        btn.setText(f"{product.name}\n₹{product.price:.2f}")
        btn.setFont(QFont("Arial", 9, QFont.Bold))
        btn.setCheckable(True)
        btn.setStyleSheet(GlobalStyles.GLOBAL_STYLE)
        btn.clicked.connect(lambda: self._select_product(btn, product))
        return btn

    def _get_icon(self, image_path) -> QIcon:
        full_path = os.path.join(IMAGE_DIR, image_path) if image_path else ""
        if os.path.exists(full_path):
            return QIcon(full_path)
        else:
            pix = QPixmap(PRODUCT_ICON_SIZE, PRODUCT_ICON_SIZE)
            pix.fill(Qt.lightGray)
            return QIcon(pix)

    def _select_product(self, btn, product):
        # Uncheck old
        if self.selected_btn:
            self.selected_btn.setChecked(False)

        # Select new
        btn.setChecked(True)
        self.selected_btn = btn
        self.selected_product = product

    def _get_current_tab(self):
        return self.tabs[list(self.tabs.keys())[self.tab_widget.currentIndex()]]

    def _add_product(self):
        dlg = ProductEditorDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            self._refresh_tabs()

    def _edit_product(self):
        if not self.selected_product:
            QMessageBox.warning(self, "No Selection", "Please select a product to edit.")
            return
        dlg = ProductEditorDialog(self, product=self.selected_product)
        if dlg.exec_() == QDialog.Accepted:
            self._refresh_tabs()

    def _delete_product(self):
        if not self.selected_product:
            QMessageBox.warning(self, "No Selection", "Please select a product to delete.")
            return
        name = self.selected_product.name
        confirm = QMessageBox.question(
            self, "Confirm Delete", f"Delete product '{name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.dao.delete_by_name(name)
            self._refresh_tabs()

    def _refresh_tabs(self):
        for tab in self.tabs.values():
            self._load_grid(tab)
        self.selected_product = None
        self.selected_btn = None

    def showEvent(self, event):
        super().showEvent(event)
        self._refresh_tabs()
