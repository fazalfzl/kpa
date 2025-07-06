from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QHBoxLayout
from .billing_item import BillingListItem


class BillingItemData:
    def __init__(self, item_count, item_name, qty, price):
        self.item_count, self.item_name, self.qty, self.price = item_count, item_name, qty, price

    def total(self):
        return self.qty * self.price


class BillingList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.customer_data = {f"C{i}": [] for i in range(1, 4)}
        self.item_counters = {f"C{i}": 1 for i in range(1, 4)}
        self.current_customer = "C1"
        self.selected_item_widget = None
        self.item_widgets = []
        self.selected_field_name = None
        self._setup_ui()
        self._display_current_customer_items()

    def set_keypad(self, keypad):
        self.keypad = keypad

    def _scroll_to_bottom(self):
        QTimer.singleShot(10,
                          lambda: self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum()))

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.scroll = QScrollArea()  # store scroll reference
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: #fafafa; }")

        self.container = QWidget()  # store container reference
        self.container.setStyleSheet("QWidget { background-color: #fafafa; }")

        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setSpacing(3)
        self.list_layout.setContentsMargins(5, 5, 5, 5)
        self.list_layout.addStretch()

        self.scroll.setWidget(self.container)
        self.main_layout.addWidget(self.scroll)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def switch_customer(self, customer_id):
        if customer_id in self.customer_data:
            self.current_customer = customer_id
            self.selected_item_widget = None
            self._display_current_customer_items()

    def _display_current_customer_items(self):
        self._clear_display()
        for item_data in self.customer_data[self.current_customer]:
            self._add_item_to_display(item_data)

    def _clear_display(self):
        self.item_widgets.clear()
        self.selected_item_widget = None
        while self.list_layout.count() > 1:
            child = self.list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _reset_keypad_if_available(self):
        if hasattr(self, 'keypad') and self.keypad:
            self.keypad.reset_input()

    def _deselect_current_item(self):
        if self.selected_item_widget:
            self.selected_item_widget.set_selected(False)

    def _on_item_clicked(self, clicked_item):
        self._reset_keypad_if_available()
        self._deselect_current_item()

        self.selected_item_widget = clicked_item
        clicked_item.set_selected(True)

        if self.selected_field_name:
            clicked_item.select_field(self.selected_field_name)

    def add_item(self, name: str, qty: int, price: float):
        count = self.item_counters[self.current_customer]
        item_data = BillingItemData(count, name, qty, price)
        self.customer_data[self.current_customer].append(item_data)
        self.item_counters[self.current_customer] += 1
        self._add_item_to_display(item_data)

    def _remove_stretch_spacer(self):
        if self.list_layout.count() > 0:
            last = self.list_layout.takeAt(self.list_layout.count() - 1)
            if last and last.spacerItem():
                del last

    def _add_item_to_display(self, item_data: BillingItemData):
        self._remove_stretch_spacer()
        self._deselect_current_item()

        item = BillingListItem(item_data)
        item.item_data = item_data
        item.item_clicked.connect(self._on_item_clicked)
        item.field_selected.connect(self._on_field_selected)

        self.item_widgets.append(item)
        self.list_layout.addWidget(item)

        self.selected_item_widget = item
        item.set_selected(True)
        self.list_layout.addStretch()

        if self.selected_field_name:
            item.select_field(self.selected_field_name)

        self._scroll_to_bottom()  # 👈 ensures item is visible

    def _on_field_selected(self, item, field):
        self._reset_keypad_if_available()

        # Deselect all other items
        for w in self.item_widgets:
            if w != item:
                w.set_selected(False)
                w.selected_field = None
                w._update_field_highlight()

        self.selected_item_widget = item
        self.selected_field_name = field
        item.set_selected(True)

    def remove_selected_item(self):
        if not self.selected_item_widget:
            return

        selected_id = self.selected_item_widget.item_data.item_count
        self.customer_data[self.current_customer] = [
            item for item in self.customer_data[self.current_customer]
            if item.item_count != selected_id
        ]
        self._renumber_items()
        self._display_current_customer_items()
        self._select_last_item()

    def _select_last_item(self):
        self.selected_item_widget = self.item_widgets[-1] if self.item_widgets else None
        if self.selected_item_widget:
            self.selected_item_widget.set_selected(True)

    def _renumber_items(self):
        items = self.customer_data[self.current_customer]
        for idx, item in enumerate(items):
            item.item_count = idx + 1
        self.item_counters[self.current_customer] = len(items) + 1

    def clear_current_customer(self):
        self.customer_data[self.current_customer] = []
        self.item_counters[self.current_customer] = 1
        self.selected_item_widget = None
        self._clear_display()

    def get_current_customer_total(self):
        return sum(item.total() for item in self.customer_data[self.current_customer])

    def get_current_customer_items(self):
        return self.customer_data[self.current_customer].copy()

    def get_current_customer(self):
        return self.current_customer
