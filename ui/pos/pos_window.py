import os
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon, QPixmap
from utils.styles import GlobalStyles, ProductStyles, ProductButtonStyles, MainContentStyles
from utils.constants import (
    IMAGE_DIR, PRODUCTS_PER_ROW, PRODUCT_GRID_SPACING,
    PRODUCT_BUTTON_WIDTH, PRODUCT_BUTTON_HEIGHT, PRODUCT_ICON_SIZE,
    BILLING_SECTION_WIDTH, PRODUCT_BUTTON_FONT_FAMILY, PRODUCT_BUTTON_FONT_SIZE,
    DEFAULT_CATEGORY
)
from .billing.billing_section import BillingSection
from ..custom_title_bar import CustomTitleBar
from database.product_dao import ProductDAO

class ProductsSection:
    def __init__(self):
        self.dao = ProductDAO()
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

        products = self.dao.get_by_category(self.current_category)
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
            img_file = product.image_path if os.path.isabs(product.image_path) else os.path.join(IMAGE_DIR, product.image_path)
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

class POSWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_content = MainContent()
        self.billing_section = BillingSection()
        self.product_dao = ProductDAO()
        self.init_ui()
        self._wire_connections()

    def init_ui(self):
        self.setWindowTitle("My POS System")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title bar
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Content area
        content_layout = QHBoxLayout()
        content_widget = QWidget()
        content_widget.setLayout(content_layout)

        # Products and billing
        left_frame = self.main_content.create_main_content_area()
        content_layout.addWidget(left_frame, 3)

        billing_frame = self.billing_section.create_billing_section()
        billing_frame.setFixedWidth(BILLING_SECTION_WIDTH)
        content_layout.addWidget(billing_frame, 1)

        main_layout.addWidget(content_widget)
        self.setStyleSheet(GlobalStyles.GLOBAL_STYLE)

    def _wire_connections(self):
        ps, bl = self.main_content.products_sec, self.billing_section.billing_list
        ps.on_product_click = lambda prod: bl.add_item(name=prod.name, qty=1, price=prod.price)

        self.title_bar.show_category.connect(self._on_category_changed)
        self.title_bar.barcode_scanned.connect(self._on_barcode_scanned)

        self.main_content.products_sec.set_category(DEFAULT_CATEGORY)

    def _on_category_changed(self, category):
        self.main_content.products_sec.set_category(category)

    def _on_barcode_scanned(self, barcode):
        try:
            product = self.product_dao.get_by_barcode(barcode)
            if product:
                self.billing_section.billing_list.add_item(name=product.name, qty=1, price=product.price)
                print(f"Added scanned product: {product.name}")
            else:
                QMessageBox.warning(self, "Product Not Found", f"No product found with barcode: {barcode}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error scanning barcode: {str(e)}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)
