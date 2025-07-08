from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from ui.billing.billing_list.item_widget import BillingListItem
from ui.billing.billing_list.logic import BillingListLogic
from ui.utils.styles import BillingListStyles


class BillingListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = BillingListLogic(self)
        self.logic.set_ui(self)
        self._selected_field_name = None

        self._setup_ui()
        self._display_current_customer_items()

    def set_keypad(self, keypad):
        self.logic.keypad = keypad

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(BillingListStyles.SCROLL_STYLE)

        self.container = QWidget()
        self.container.setStyleSheet(BillingListStyles.CONTAINER_STYLE)

        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setSpacing(3)
        self.list_layout.setContentsMargins(5, 5, 5, 5)
        self.list_layout.addStretch()

        self.scroll.setWidget(self.container)
        self.main_layout.addWidget(self.scroll)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def _scroll_to_bottom(self):
        QTimer.singleShot(10, lambda: self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum()))

    def _display_current_customer_items(self):
        self._clear_display()
        for item_data in self.logic.get_current_customer_items():
            self._add_item_to_display(item_data)

    def _clear_display(self):
        self.logic.item_widgets.clear()
        self.logic.selected_item_widget = None
        while self.list_layout.count() > 1:
            child = self.list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _add_item_to_display(self, item_data):
        self._remove_stretch_spacer()
        self._deselect_current_item()

        item = BillingListItem(item_data)
        item.item_clicked.connect(self.logic._on_item_clicked)
        item.fieldFocused.connect(self.logic._on_fieldFocused)

        self.logic.item_widgets.append(item)
        self.list_layout.addWidget(item)

        self.logic.selected_item_widget = item
        item.set_selected(True)
        self.list_layout.addStretch()

        if self.selected_field_name:
            item.select_field(self.selected_field_name)

        self._scroll_to_bottom()

    def _remove_stretch_spacer(self):
        if self.list_layout.count() > 0:
            last = self.list_layout.takeAt(self.list_layout.count() - 1)
            if last and last.spacerItem():
                del last

    def _deselect_current_item(self):
        if self.logic.selected_item_widget:
            self.logic.selected_item_widget.set_selected(False)

    def add_item(self, name, qty, price):
        self.logic.add_item(name, qty, price)

    def remove_selected_item(self):
        self.logic.remove_selected_item()

    @property
    def selected_item_widget(self):
        return self.logic.selected_item_widget

    @property
    def selected_field_name(self):
        return self._selected_field_name

    @selected_field_name.setter
    def selected_field_name(self, value):
        self._selected_field_name = value

    def get_current_customer_total(self):
        return self.logic.get_current_customer_total()

    def get_current_customer_items(self):
        return self.logic.get_current_customer_items()

    def get_current_customer(self):
        return self.logic.get_current_customer()

    def switch_customer(self, customer_id):
        self.logic.switch_customer(customer_id)
    def clear_current_customer(self):
        self.logic.clear_current_customer()


