from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class BillingListItem(QFrame):
    item_clicked = pyqtSignal(object)
    field_selected = pyqtSignal(object, str)

    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.item_data = item_data
        self.selected_field = None
        self.is_selected = False

        self.setFrameShape(QFrame.StyledPanel)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(60)
        self._update_style()
        self._setup_layout()

    def _setup_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 4, 6, 4)
        main_layout.setSpacing(2)
        main_layout.addLayout(self._create_top_row())
        main_layout.addLayout(self._create_bottom_row())

    def _update_style(self):
        style = """
            QFrame {
                border: 2px solid #4CAF50;
                border-radius: 4px;
                background-color: #f0f8f0;
            }
        """ if self.is_selected else """
            QFrame {
                border: 1px solid #999;
                border-radius: 4px;
                background-color: #fff;
            }
            QFrame:hover {
                background-color: #f5f5f5;
            }
        """
        self.setStyleSheet(style)

    def set_selected(self, selected):
        self.is_selected = selected
        self._update_style()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.item_clicked.emit(self)
        super().mousePressEvent(event)

    def _create_label(self, text, font_size, font_weight=QFont.Normal, color="#333", extra_style="", alignment=Qt.AlignLeft | Qt.AlignVCenter):
        label = QLabel(text)
        label.setFont(QFont("Arial", font_size, font_weight))
        label.setStyleSheet(f"color: {color}; {extra_style}")
        label.setAlignment(alignment)
        return label

    def _create_top_row(self):
        layout = QHBoxLayout()

        count_label = self._create_label(
            f"#{self.item_data.item_count}", 9, QFont.Bold, "#666",
            "background-color: #f0f0f0; border-radius: 3px; padding: 2px 4px;",
            Qt.AlignCenter
        )
        count_label.setFixedWidth(32)

        name_label = self._create_label(
            self.item_data.item_name, 11, QFont.Bold
        )

        layout.addWidget(count_label)
        layout.addWidget(name_label, 1)
        return layout

    def _create_clickable_label(self, text, field_name):
        label = self._create_label(text, 9, color="#555")
        label.mousePressEvent = lambda e: self.select_field(field_name)
        return label

    def _create_bottom_row(self):
        layout = QHBoxLayout()

        self.qty_label = self._create_clickable_label(f"Qty: {self.item_data.qty}", "qty")
        self.price_label = self._create_clickable_label(f"Price: ₹{self.item_data.price:.2f}", "price")
        self.amount_label = self._create_label(
            f"₹{self.item_data.total():.2f}", 10, QFont.Bold, "#2E8B57",
            alignment=Qt.AlignRight | Qt.AlignVCenter
        )

        layout.addWidget(self.qty_label)
        layout.addWidget(self.price_label)
        layout.addStretch()
        layout.addWidget(self.amount_label)

        return layout

    def _update_field_highlight(self):
        highlight_style = (
            "color: #222;"
            "background-color: #cceeff;"  # Bright visible highlight
            "border: 2px solid #007acc;"  # Bold visible border
            "border-radius: 3px;"
        )

        default_style = (
            "color: #222;"
            "background-color: #ffffff;"  # White background
            "border: 1px solid #bbb;"  # Subtle but visible border
            "border-radius: 3px;"
        )

        field_styles = {
            "qty": highlight_style if self.selected_field == "qty" else default_style,
            "price": highlight_style if self.selected_field == "price" else default_style,
        }

        self.qty_label.setStyleSheet(field_styles["qty"])
        self.price_label.setStyleSheet(field_styles["price"])

    def select_field(self, field_name):
        if field_name in ("qty", "price"):
            self.selected_field = field_name
            self._update_field_highlight()
            self.field_selected.emit(self, field_name)

