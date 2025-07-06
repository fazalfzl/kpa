from PyQt5.QtWidgets import QPushButton
from utils.styles import KeypadStyles
from utils.constants import BUTTON_SIZE


class Keypad:
    def __init__(self):
        self.buttons = {}
        self.billing_list = None
        self.input_buffer = ""

    def set_billing_list(self, billing_list):
        self.billing_list = billing_list

    def add_to_layout(self, layout):
        """Add all keypad buttons to the given layout"""
        # Numeric keypad buttons
        # Row 1: 1, 2, 3
        for i, num in enumerate([1, 2, 3]):
            btn = self.create_number_button(num)
            layout.addWidget(btn, 0, i + 1)

        # Row 2: 4, 5, 6
        for i, num in enumerate([4, 5, 6]):
            btn = self.create_number_button(num)
            layout.addWidget(btn, 1, i + 1)

        # Row 3: 7, 8, 9
        for i, num in enumerate([7, 8, 9]):
            btn = self.create_number_button(num)
            layout.addWidget(btn, 2, i + 1)

        # Bottom row: ., 0, X
        decimal_btn = self.create_operation_button(".", KeypadStyles.PLUS_MINUS_STYLE)
        layout.addWidget(decimal_btn, 3, 1)

        zero_btn = self.create_number_button(0)
        layout.addWidget(zero_btn, 3, 2)

        clear_btn = self.create_operation_button("X", KeypadStyles.CLEAR_STYLE)
        layout.addWidget(clear_btn, 3, 3)

    def create_number_button(self, number):
        """Create a number button"""
        btn = QPushButton(str(number))
        btn.setStyleSheet(KeypadStyles.NUMBER_STYLE)
        btn.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        btn.clicked.connect(lambda: self.number_clicked(number))
        self.buttons[str(number)] = btn
        return btn

    def create_operation_button(self, text, style):
        """Create an operation button (., X)"""
        btn = QPushButton(text)
        btn.setStyleSheet(style)
        btn.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        btn.clicked.connect(lambda: self.button_clicked(text))
        self.buttons[text] = btn
        return btn

    def number_clicked(self, number):
        print(f"Number clicked: {number}")
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

        except ValueError:
            pass

    def button_clicked(self, button_name):
        """Handle operation button clicks"""
        print(f"Button clicked: {button_name}")
        if button_name == "X":
            self.input_buffer = ""
            self._apply_input()
        elif button_name == ".":
            # Add decimal point only if not already present
            if "." not in self.input_buffer:
                # If buffer is empty, start with "0."
                if not self.input_buffer:
                    self.input_buffer = "0."
                else:
                    self.input_buffer += "."
                self._apply_input()

    def reset_input(self):
        self.input_buffer = ""
