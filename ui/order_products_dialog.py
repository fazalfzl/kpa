from PyQt5.QtWidgets import *
from database.product_repository import ProductRepository

class OrderProductsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Order Products")
        self.dao, self.current_category, self.products = ProductRepository(), "fruits_veg", []
        self._build_ui()
        self._load_products()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Category selector
        cat_layout = QHBoxLayout()
        cat_layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Fruits & Vegetables", "Manual"])
        self.category_combo.currentTextChanged.connect(self._on_category_changed)
        cat_layout.addWidget(self.category_combo)
        cat_layout.addStretch()
        layout.addLayout(cat_layout)

        # Products list
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Move buttons
        btn_layout = QHBoxLayout()
        for text, slot in [("Move Up", self._move_up), ("Move Down", self._move_down)]:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        # Save/Cancel
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        for text, slot in [("Save & Close", self.accept), ("Cancel", self.reject)]:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            save_layout.addWidget(btn)
        layout.addLayout(save_layout)

    def _on_category_changed(self, text):
        self.current_category = {"Fruits & Vegetables": "fruits_veg", "Manual": "manual"}[text]
        self._load_products()

    def _load_products(self):
        self.list_widget.clear()
        self.products = self.dao.get_by_category(self.current_category)
        [self.list_widget.addItem(f"{p.name} (${p.price:.2f})") for p in self.products]

    def _move_up(self):
        self._move(-1)

    def _move_down(self):
        self._move(1)

    def _move(self, direction):
        row = self.list_widget.currentRow()
        target = row + direction
        if 0 <= target < len(self.products):
            self.dao.swap_order(self.products[row].id, self.products[target].id)
            self._load_products()
