from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel, QMenu, QAction, QDialog,
    QLineEdit, QMessageBox
)
from ui.pos.edit_product_dialog import ProductEditorDialog
from ui.pos.order_products_dialog import OrderProductsDialog
from ui.pos.product_management_dialog import ProductManagementDialog
from utils.print_pkg.printer_config import PrinterTester
from utils.styles import (
    TitleBarStyles, CategoryButtonStyles, BarcodeInputStyles, TitleLabelStyles
)
from utils.constants import (
    TITLE_BAR_HEIGHT, TITLE_BAR_MARGIN, TITLE_BAR_SPACING, TITLE_BAR_LEFT_SPACING,
    MENU_BUTTON_SIZE, WINDOW_CONTROL_BUTTON_SIZE, FRUITS_BUTTON_WIDTH, FRUITS_BUTTON_HEIGHT,
    MANUAL_BUTTON_WIDTH, MANUAL_BUTTON_HEIGHT, BARCODE_INPUT_WIDTH, BARCODE_INPUT_HEIGHT,
    TITLE_BAR_FONT_FAMILY, TITLE_BAR_FONT_SIZE, MENU_BUTTON_FONT_SIZE,
    WINDOW_CONTROL_FONT_SIZE, MAXIMIZE_BUTTON_FONT_SIZE, APP_TITLE, BARCODE_PLACEHOLDER
)


class CustomTitleBar(QWidget):
    # signals to communicate with POSWindow
    show_category = pyqtSignal(str)  # "fruits_veg" or "manual"
    barcode_scanned = pyqtSignal(str)  # barcode string

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.start = QPoint(0, 0)
        self.pressing = False

    def init_ui(self):
        self.setFixedHeight(TITLE_BAR_HEIGHT)
        self.setStyleSheet(TitleBarStyles.TITLE_BAR_STYLE)

        layout = QHBoxLayout()
        layout.setContentsMargins(TITLE_BAR_MARGIN, 0, TITLE_BAR_MARGIN, 0)
        layout.setSpacing(TITLE_BAR_SPACING)

        # Left side - Menu button and title
        left_layout = QHBoxLayout()
        left_layout.setSpacing(TITLE_BAR_LEFT_SPACING)

        # Menu button
        self.menu_btn = QPushButton("☰")
        self.menu_btn.setFixedSize(MENU_BUTTON_SIZE, MENU_BUTTON_SIZE)
        self.menu_btn.setStyleSheet(TitleBarStyles.MENU_BUTTON_STYLE)
        self.menu_btn.setFont(QFont(TITLE_BAR_FONT_FAMILY, MENU_BUTTON_FONT_SIZE))
        self.menu_btn.clicked.connect(self.show_menu)
        left_layout.addWidget(self.menu_btn)

        # App title
        self.title_label = QLabel(APP_TITLE)
        self.title_label.setFont(QFont(TITLE_BAR_FONT_FAMILY, TITLE_BAR_FONT_SIZE, QFont.Bold))
        self.title_label.setStyleSheet(TitleLabelStyles.LABEL_STYLE)
        left_layout.addWidget(self.title_label)

        # Middle - Category buttons and barcode input
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(TITLE_BAR_SPACING)

        # Category buttons
        self.fruits_btn = QPushButton("🍏 Fruits & Veg")
        self.fruits_btn.setFixedSize(FRUITS_BUTTON_WIDTH, FRUITS_BUTTON_HEIGHT)
        self.fruits_btn.setStyleSheet(CategoryButtonStyles.FRUITS_BUTTON_STYLE)
        self.fruits_btn.clicked.connect(lambda: self.show_category.emit("fruits_veg"))
        middle_layout.addWidget(self.fruits_btn)

        self.manual_btn = QPushButton("📦 Manual")
        self.manual_btn.setFixedSize(MANUAL_BUTTON_WIDTH, MANUAL_BUTTON_HEIGHT)
        self.manual_btn.setStyleSheet(CategoryButtonStyles.MANUAL_BUTTON_STYLE)
        self.manual_btn.clicked.connect(lambda: self.show_category.emit("manual"))
        middle_layout.addWidget(self.manual_btn)

        # Barcode input
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText(BARCODE_PLACEHOLDER)
        self.barcode_input.setFixedSize(BARCODE_INPUT_WIDTH, BARCODE_INPUT_HEIGHT)
        self.barcode_input.setStyleSheet(BarcodeInputStyles.INPUT_STYLE)
        self.barcode_input.returnPressed.connect(self._on_barcode_entered)
        middle_layout.addWidget(self.barcode_input)

        # Right side - Window controls
        right_layout = QHBoxLayout()
        right_layout.setSpacing(5)

        # Minimize button
        self.minimize_btn = QPushButton("−")
        self.minimize_btn.setFixedSize(WINDOW_CONTROL_BUTTON_SIZE, WINDOW_CONTROL_BUTTON_SIZE)
        self.minimize_btn.setStyleSheet(TitleBarStyles.MINIMIZE_BUTTON_STYLE)
        self.minimize_btn.setFont(QFont(TITLE_BAR_FONT_FAMILY, WINDOW_CONTROL_FONT_SIZE, QFont.Bold))
        self.minimize_btn.clicked.connect(self.minimize_window)
        right_layout.addWidget(self.minimize_btn)

        # Maximize/Restore button
        self.maximize_btn = QPushButton("□")
        self.maximize_btn.setFixedSize(WINDOW_CONTROL_BUTTON_SIZE, WINDOW_CONTROL_BUTTON_SIZE)
        self.maximize_btn.setStyleSheet(TitleBarStyles.MAXIMIZE_BUTTON_STYLE)
        self.maximize_btn.setFont(QFont(TITLE_BAR_FONT_FAMILY, MAXIMIZE_BUTTON_FONT_SIZE, QFont.Bold))
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        right_layout.addWidget(self.maximize_btn)

        # Close button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(WINDOW_CONTROL_BUTTON_SIZE, WINDOW_CONTROL_BUTTON_SIZE)
        self.close_btn.setStyleSheet(TitleBarStyles.CLOSE_BUTTON_STYLE)
        self.close_btn.setFont(QFont(TITLE_BAR_FONT_FAMILY, WINDOW_CONTROL_FONT_SIZE, QFont.Bold))
        self.close_btn.clicked.connect(self.close_application)
        right_layout.addWidget(self.close_btn)

        # Add all layouts to main layout
        layout.addLayout(left_layout)
        layout.addLayout(middle_layout)
        layout.addStretch()  # Push window controls to the right
        layout.addLayout(right_layout)

        self.setLayout(layout)

    def _on_barcode_entered(self):
        """Handle barcode input when Enter is pressed"""
        barcode = self.barcode_input.text().strip()
        if barcode:
            self.barcode_scanned.emit(barcode)
            self.barcode_input.clear()

    def show_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet(TitleBarStyles.MENU_STYLE)

        # Create Product
        create_act = QAction("➕ Create Product", self)
        create_act.triggered.connect(self._open_create_product)
        menu.addAction(create_act)

        # Order Products
        order_act = QAction("↕️ Order Products", self)
        order_act.triggered.connect(self._open_order_products)
        menu.addAction(order_act)

        manage_products_action = QAction("🛠️ Manage Products", self)
        manage_products_action.triggered.connect(self._open_product_management)
        menu.addAction(manage_products_action)

        menu.addSeparator()

        # Add menu items
        file_action = QAction("📁 File", self)
        file_action.triggered.connect(lambda: print("File menu clicked"))
        menu.addAction(file_action)

        settings_action = QAction("⚙️ Settings", self)
        settings_action.triggered.connect(lambda: print("Settings clicked"))
        menu.addAction(settings_action)

        menu.addSeparator()

        reports_action = QAction("📊 Reports", self)
        reports_action.triggered.connect(lambda: print("Reports clicked"))
        menu.addAction(reports_action)

        inventory_action = QAction("📦 Inventory", self)
        inventory_action.triggered.connect(lambda: print("Inventory clicked"))
        menu.addAction(inventory_action)

        menu.addSeparator()

        help_action = QAction("❓ Help", self)
        help_action.triggered.connect(lambda: print("Help clicked"))
        menu.addAction(help_action)

        about_action = QAction("ℹ️ About", self)
        about_action.triggered.connect(lambda: print("About clicked"))
        menu.addAction(about_action)

        # Add Test Printer option
        test_printer_action = QAction("🖨️ Test Printer", self)
        test_printer_action.triggered.connect(self._test_printer)
        menu.addAction(test_printer_action)

        # Show menu below the menu button
        pos = self.menu_btn.mapToGlobal(QPoint(0, self.menu_btn.height()))
        menu.exec_(pos)

    def _test_printer(self):
        """Test the printer by printing 'Hello World'."""
        tester = PrinterTester()
        tester.run()
        tester.test_printer()

    def _open_product_management(self):
        dlg = ProductManagementDialog(self.parent)
        dlg.exec_()

    def _open_create_product(self):
        dlg = ProductEditorDialog(self.parent)
        if dlg.exec_() == QDialog.Accepted:
            self.parent.main_content.products_sec.refresh()

    def _open_order_products(self):
        dlg = OrderProductsDialog(self.parent)
        if dlg.exec_() == QDialog.Accepted:
            self.parent.main_content.products_sec.refresh()

    def minimize_window(self):
        """Minimize the window"""
        if self.parent:
            self.parent.showMinimized()

    def toggle_maximize(self):
        """Toggle between maximized and normal window state"""
        if self.parent:
            if self.parent.isMaximized():
                self.parent.showNormal()
                self.maximize_btn.setText("□")
            else:
                self.parent.showMaximized()
                self.maximize_btn.setText("❐")

    def close_application(self):
        """Close the application"""
        if self.parent:
            self.parent.close()

    def mousePressEvent(self, event):
        """Handle mouse press for window dragging"""
        if event.button() == Qt.LeftButton:
            self.start = self.mapToGlobal(event.pos())
            self.pressing = True

    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging"""
        if self.pressing and self.parent:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                  self.mapToGlobal(self.movement).y(),
                                  self.parent.width(),
                                  self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        self.pressing = False