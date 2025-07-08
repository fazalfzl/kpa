from PyQt5.QtWidgets import QWidget

from ui.billing.keypad.ui import BillingKeypadUI
from ui.billing.action_buttons.logic import ActionButtonsLogic


class BillingKeypad(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.billing_list = None
        self.input_buffer = ""
        self.ui = BillingKeypadUI(self)

    def set_billing_list(self, billing_list):
        self.billing_list = billing_list

    def number_clicked(self, number):
        if not self.billing_list or not self.billing_list.selected_item_widget:
            return
        self.input_buffer += str(number)
        self._apply_input()

    def _apply_input(self):
        item = self.billing_list.selected_item_widget
        field = self.billing_list.selected_field_name
        if not item or not field:
            return
        try:
            if field == "qty":
                item.item_data.qty = int(self.input_buffer)
                item.qty_label.setText(f"Qty: {item.item_data.qty}")
            elif field == "price":
                item.item_data.price = float(self.input_buffer)
                item.price_label.setText(f"Price: ₹{item.item_data.price:.2f}")
            item.amount_label.setText(f"₹{item.item_data.total():.2f}")

            # 🔁 live update total
            if hasattr(self.billing_list, 'action_buttons_logic'):
                self.billing_list.action_buttons_logic.update_bill_amount()

        except ValueError:
            pass

    def button_clicked(self, button_name):
        if button_name == "X":
            self.input_buffer = ""
            self._apply_input()
        elif button_name == ".":
            if "." not in self.input_buffer:
                self.input_buffer += "." if self.input_buffer else "0."
                self._apply_input()

    def reset_input(self):
        self.input_buffer = ""

    def add_to_layout(self, layout):
        self.ui.add_buttons_to(layout)
