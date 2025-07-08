import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import *

from core.services.product_service import ProductService
from utils.constants import (
    IMAGE_DIR, PRODUCTS_PER_ROW, PRODUCT_GRID_SPACING,
    PRODUCT_BUTTON_WIDTH, PRODUCT_BUTTON_HEIGHT, PRODUCT_ICON_SIZE,
    PRODUCT_BUTTON_FONT_FAMILY, PRODUCT_BUTTON_FONT_SIZE,
    DEFAULT_CATEGORY
)
from ui.utils.styles import ProductStyles, ProductButtonStyles, MainContentStyles


class ProductsSection:
    def __init__(self):
        self.service = ProductService()
        self.container = self.scroll_area = None
        self.current_category = DEFAULT_CATEGORY
        self.on_product_click = None

    def create_products_section(self):
        self.container = QFrame()
        self.container.setStyleSheet(ProductStyles.FRAME_STYLE)
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.scroll_area = self._make_scroll_area()
        layout.addWidget(self.scroll_area)
        return self.container

    def set_category(self, category):
        self.current_category = category
        self.refresh()

    def refresh(self):
        if not self.container or not self.scroll_area:
            return
        layout = self.container.layout()
        layout.removeWidget(self.scroll_area)
        self.scroll_area.deleteLater()
        self.scroll_area = self._make_scroll_area()
        layout.addWidget(self.scroll_area)

    def _make_scroll_area(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        holder = QWidget()
        grid = QGridLayout(holder)
        grid.setSpacing(PRODUCT_GRID_SPACING)

        products = self.service.get_by_category(self.current_category)
        for idx, p in enumerate(products):
            btn = self._make_button(p)
            grid.addWidget(btn, idx // PRODUCTS_PER_ROW, idx % PRODUCTS_PER_ROW, Qt.AlignCenter)

        scroll.setWidget(holder)
        return scroll

    def _make_button(self, product):
        btn = QToolButton()
        btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn.setFixedSize(PRODUCT_BUTTON_WIDTH, PRODUCT_BUTTON_HEIGHT)
        btn.setIcon(self._load_icon(product))
        btn.setIconSize(QSize(PRODUCT_ICON_SIZE, PRODUCT_ICON_SIZE))
        btn.setText(f"{product.name}\n${product.price:.2f}")
        btn.setFont(QFont(PRODUCT_BUTTON_FONT_FAMILY, PRODUCT_BUTTON_FONT_SIZE, QFont.Bold))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(ProductButtonStyles.BUTTON_STYLE)
        btn.clicked.connect(lambda _, p=product: self._on_click(p))
        return btn

    def _load_icon(self, product):
        if product.image_path:
            img_file = product.image_path if os.path.isabs(product.image_path) else os.path.join(IMAGE_DIR,
                                                                                                 product.image_path)
            if os.path.exists(img_file):
                return QIcon(img_file)
        pix = QPixmap(PRODUCT_ICON_SIZE, PRODUCT_ICON_SIZE)
        pix.fill(Qt.lightGray)
        return QIcon(pix)

    def _on_click(self, product):
        if product and callable(self.on_product_click):
            self.on_product_click(product)


class MainContent:
    def __init__(self):
        self.products_sec = ProductsSection()

    def create_main_content_area(self):
        frame = QWidget()
        frame.setStyleSheet(MainContentStyles.FRAME_STYLE)
        layout = QVBoxLayout(frame)
        layout.addWidget(self.products_sec.create_products_section())
        layout.setSpacing(0)
        return frame
