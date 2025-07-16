from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTabWidget, QWidget, QToolButton,
    QPushButton, QHBoxLayout, QMessageBox, QGridLayout,
    QScrollArea, QLineEdit, QSizePolicy, QLabel
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont, QPixmap

from core.services.product_service import ProductService
from ui.product.editor import ProductEditorDialog
from ui.utils.styles import GlobalStyles

import os

IMAGE_DIR = os.path.join(os.getcwd(), "product_images")
PRODUCT_ICON_SIZE = 128
PRODUCT_GRID_COLUMNS = 3


class ProductManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Product Management")
        self.service = ProductService()
        self.tabs = {}
        self.selected_btn = None
        self.selected_product = None
        self.last_selected_index = -1
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.tab_widget = QTabWidget()
        for category in ["fruits_veg", "manual", "barcode_only"]:
            self.tabs[category] = self._create_product_grid(category)
            self.tab_widget.addTab(self.tabs[category]["widget"], category.replace("_", " ").title())
        layout.addWidget(self.tab_widget)

        for tab in self.tabs.values():
            self._load_grid(tab)

        # Control Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Product")
        self.edit_btn = QPushButton("Edit Product")
        self.delete_btn = QPushButton("Delete Product")
        self.move_up_btn = QPushButton("↑ Move Up")
        self.move_down_btn = QPushButton("↓ Move Down")

        for btn in [self.edit_btn, self.delete_btn, self.move_up_btn, self.move_down_btn]:
            btn.setEnabled(False)

        self.add_btn.clicked.connect(self._add_product)
        self.edit_btn.clicked.connect(self._edit_product)
        self.delete_btn.clicked.connect(self._delete_product)
        self.move_up_btn.clicked.connect(self._move_product_up)
        self.move_down_btn.clicked.connect(self._move_product_down)

        for btn in [self.add_btn, self.edit_btn, self.delete_btn, self.move_up_btn, self.move_down_btn]:
            btn.setFixedHeight(60)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.move_up_btn)
        btn_layout.addWidget(self.move_down_btn)

        layout.addLayout(btn_layout)

    def _make_product_button(self, product, index):
        from functools import partial

        btn = QWidget()
        btn.setFixedSize(PRODUCT_ICON_SIZE + 20, 250)  # limit width to match image area
        layout = QVBoxLayout(btn)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(5, 5, 5, 5)

        icon_label = QLabel()
        icon_label.setFixedSize(PRODUCT_ICON_SIZE, PRODUCT_ICON_SIZE)
        pixmap = self._get_icon(product.image_path).pixmap(PRODUCT_ICON_SIZE, PRODUCT_ICON_SIZE)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        name_label = QLabel(product.name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(name_label)

        price_edit = QLineEdit(f"{product.price:.2f}")
        price_edit.setAlignment(Qt.AlignCenter)
        price_edit.setFont(QFont("Arial", 14, QFont.Bold))
        price_edit.setStyleSheet("padding: 10px; border: 2px solid #888;")
        price_edit.setFixedHeight(50)
        price_edit.setReadOnly(True)
        price_edit.mousePressEvent = lambda e: self._enable_price_edit(price_edit)
        price_edit.editingFinished.connect(partial(self._save_price_edit, price_edit, product))
        layout.addWidget(price_edit)

        btn.mouseDoubleClickEvent = lambda e: self._edit_product_direct(product)
        btn.mousePressEvent = lambda e: self._select_product(btn, product)

        return btn

    def _create_product_grid(self, category):
        outer_widget = QWidget()
        outer_layout = QVBoxLayout(outer_widget)

        search_layout = QHBoxLayout()
        search_field = QLineEdit()
        search_btn = QPushButton("Search")
        clear_btn = QPushButton("Clear")

        search_field.setPlaceholderText("Search products...")
        # search_field.textChanged.connect(lambda: self._filter_products(tab))

        search_layout.addWidget(search_field)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(clear_btn)

        outer_layout.addLayout(search_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        grid = QGridLayout(content_widget)
        scroll_area.setWidget(content_widget)
        outer_layout.addWidget(scroll_area)

        tab = {
            "widget": outer_widget,
            "grid": grid,
            "category": category,
            "buttons": [],
            "content_widget": content_widget,
            "search_field": search_field,
        }

        search_btn.clicked.connect(lambda: self._filter_products(tab))
        clear_btn.clicked.connect(lambda: self._clear_search(tab))

        return tab

    def _load_grid(self, tab, products=None):
        layout = tab["grid"]
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        tab["buttons"] = []
        tab["selected_btn"] = None

        if products is None:
            products = self.service.get_by_category(tab["category"])

        for i, product in enumerate(products):
            btn = self._make_product_button(product, i)
            layout.addWidget(btn, i // PRODUCT_GRID_COLUMNS, i % PRODUCT_GRID_COLUMNS)
            tab["buttons"].append((btn, product))

        if 0 <= self.last_selected_index < len(tab["buttons"]):
            btn, product = tab["buttons"][self.last_selected_index]
            self._select_product(btn, product)

    def _enable_price_edit(self, line_edit):
        line_edit.setReadOnly(False)
        line_edit.setFocus()
        line_edit.selectAll()

    def _save_price_edit(self, line_edit, product):
        try:
            new_price = float(line_edit.text())
            if new_price != product.price:
                self.service.update_product(product.id, price=new_price)
                product.price = new_price  # Update local object too
        except ValueError:
            pass
        finally:
            line_edit.setText(f"{product.price:.2f}")
            line_edit.setReadOnly(True)

    def _edit_product_direct(self, product):
        dialog = ProductEditorDialog(self, product=product)
        if dialog.exec_():
            self._refresh_current_tab()

    def _get_icon(self, image_path):
        path = os.path.join(IMAGE_DIR, image_path) if image_path else None
        if path and os.path.exists(path):
            return QIcon(path)
        placeholder = QPixmap(PRODUCT_ICON_SIZE, PRODUCT_ICON_SIZE)
        placeholder.fill(Qt.lightGray)
        return QIcon(placeholder)

    def _select_product(self, btn, product):
        for t in self.tabs.values():
            for b, _ in t["buttons"]:
                b.setStyleSheet("")
        btn.setStyleSheet("border: 3px solid blue;")
        self.selected_product = product
        self.selected_btn = btn
        self.last_selected_index = self._get_selected_index()
        for control in [self.edit_btn, self.delete_btn, self.move_up_btn, self.move_down_btn]:
            control.setEnabled(True)

    def _get_selected_index(self):
        tab = self.tabs[self._current_category()]
        for i, (_, p) in enumerate(tab["buttons"]):
            if p.id == self.selected_product.id:
                return i
        return -1

    def _filter_products(self, tab):
        text = tab["search_field"].text().strip().lower()
        # filtered = [p for p in self.service.get_by_category(tab["category"]) if text in p.name.lower()]
        # i want to also look for the barcode
        products = self.service.get_by_category(tab["category"]) or []
        filtered = [p for p in products if text in p.name.lower() or text in p.barcode]
        self._load_grid(tab, filtered)


    def _clear_search(self, tab):
        tab["search_field"].clear()
        self._load_grid(tab)

    def _add_product(self):
        dialog = ProductEditorDialog(self)
        if dialog.exec_():
            self._refresh_current_tab()

    def _edit_product(self):
        if self.selected_product:
            dialog = ProductEditorDialog(self, product=self.selected_product)
            if dialog.exec_():
                self._refresh_current_tab()

    def _delete_product(self):
        if self.selected_product:
            reply = QMessageBox.question(self, "Delete", f"Delete {self.selected_product.name}?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.service.delete_product_by_name(self.selected_product.name)
                self._refresh_current_tab()

    def _refresh_current_tab(self):
        tab = self.tabs[self._current_category()]
        self._load_grid(tab)

    def _current_category(self):
        index = self.tab_widget.currentIndex()
        return list(self.tabs.keys())[index]

    def _move_product_up(self):
        tab = self.tabs[self._current_category()]
        idx = self._get_selected_index()
        if idx > 0:
            above = tab["buttons"][idx - 1][1]
            self.service.reorder_products(self.selected_product.id, above.id)
            self.last_selected_index = idx - 1
            self._refresh_current_tab()

    def _move_product_down(self):
        tab = self.tabs[self._current_category()]
        idx = self._get_selected_index()
        if 0 <= idx < len(tab["buttons"]) - 1:
            below = tab["buttons"][idx + 1][1]
            self.service.reorder_products(self.selected_product.id, below.id)
            self.last_selected_index = idx + 1
            self._refresh_current_tab()
