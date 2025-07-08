
from PyQt5.QtCore import QObject, pyqtSignal


class BillingItemData:
    def __init__(self, item_count, item_name, qty, price):
        self.item_count, self.item_name, self.qty, self.price = item_count, item_name, qty, price

    def total(self):
        return self.qty * self.price



class BillingListLogic(QObject):
    bill_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.customer_data = {f"C{i}": [] for i in range(1, 4)}
        self.item_counters = {f"C{i}": 1 for i in range(1, 4)}
        self.current_customer = "C1"
        self.selected_item_widget = None
        self.item_widgets = []
        self.keypad = None
        self.ui = None

    def set_ui(self, ui):
        self.ui = ui

    def _reset_keypad_if_available(self):
        if self.keypad:
            self.keypad.reset_input()

    def _on_item_clicked(self, clicked_item):
        self._reset_keypad_if_available()
        if self.selected_item_widget:
            self.selected_item_widget.set_selected(False)

        self.selected_item_widget = clicked_item
        clicked_item.set_selected(True)

        if self.ui.selected_field_name:
            clicked_item.select_field(self.ui.selected_field_name)

    def _on_fieldFocused(self, item, field):
        self._reset_keypad_if_available()

        for w in self.item_widgets:
            if w != item:
                w.set_selected(False)
                w.selected_field = None
                w._update_field_highlight()

        self.selected_item_widget = item
        self.ui.selected_field_name = field
        item.set_selected(True)

    def switch_customer(self, customer_id):
        if customer_id in self.customer_data:
            self.current_customer = customer_id
            self.selected_item_widget = None
            self.ui._display_current_customer_items()

    def add_item(self, name: str, qty: int, price: float):
        count = self.item_counters[self.current_customer]
        item_data = BillingItemData(count, name, qty, price)
        self.customer_data[self.current_customer].append(item_data)
        self.item_counters[self.current_customer] += 1
        self.ui._add_item_to_display(item_data)
        self.bill_changed.emit()  # 🔁 emit on add

    def remove_selected_item(self):
        if not self.selected_item_widget:
            return

        selected_id = self.selected_item_widget.item_data.item_count
        self.customer_data[self.current_customer] = [
            item for item in self.customer_data[self.current_customer]
            if item.item_count != selected_id
        ]

        self._renumber_items()
        self.ui._display_current_customer_items()
        self._select_last_item()
        self.bill_changed.emit()  # 🔁 emit on delete

    def _renumber_items(self):
        items = self.customer_data[self.current_customer]
        for idx, item in enumerate(items):
            item.item_count = idx + 1
        self.item_counters[self.current_customer] = len(items) + 1

    def _select_last_item(self):
        self.selected_item_widget = self.item_widgets[-1] if self.item_widgets else None
        if self.selected_item_widget:
            self.selected_item_widget.set_selected(True)

    def clear_current_customer(self):
        self.customer_data[self.current_customer] = []
        self.item_counters[self.current_customer] = 1
        self.selected_item_widget = None
        self.ui._clear_display()

    def get_current_customer_total(self):
        return sum(item.total() for item in self.customer_data[self.current_customer])

    def get_current_customer_items(self):
        return self.customer_data[self.current_customer].copy()

    def get_current_customer(self):
        return self.current_customer
