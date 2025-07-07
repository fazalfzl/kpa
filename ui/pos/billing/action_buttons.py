from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.print_pkg.printer_config import PrinterTester
from utils.styles import ActionButtonStyles
from utils.constants import ACTION_BUTTON_WIDTH, ACTION_BUTTON_HEIGHT, BUTTON_SIZE

class ActionButtons:
    def __init__(self):
        self.buttons = {}
        self.billing_list = None
        self.current_customer = "C1"  # Track current customer
        self.printer_tester = PrinterTester()  # Single instance of PrinterTester

    def set_billing_list(self, billing_list):
        """Set the billing list reference for adding items"""
        self.billing_list = billing_list
        print(f"Billing list connected to ActionButtons")

    def set_current_customer(self, customer_id):
        """Set the current customer for the action buttons"""
        self.current_customer = customer_id
        print(f"Action buttons now working with: {customer_id}")

    def add_to_layout(self, layout):
        """Add all action buttons to the given layout"""
        # Action buttons
        add_row_btn = self.create_action_button("ADD ROW", ActionButtonStyles.ADD_ROW_STYLE)
        delete_row_btn = self.create_action_button("DELETE ROW", ActionButtonStyles.DELETE_ROW_STYLE)
        price_btn = self.create_action_button("PRICE", ActionButtonStyles.PRICE_STYLE)
        qty_btn = self.create_action_button("QTY", ActionButtonStyles.QTY_STYLE)

        # Position action buttons
        layout.addWidget(add_row_btn, 0, 0, 1, 1)  # Above '1'
        layout.addWidget(delete_row_btn, 1, 0, 1, 1)  # Above '4'
        layout.addWidget(price_btn,   1, 4, 1, 1) # Right of '3'
        layout.addWidget(qty_btn,0, 4, 1, 1)  # Right of '6'

        # Bill amount display
        bill_amount_label = self.create_bill_amount_display()
        layout.addWidget(bill_amount_label, 2, 0, 1, 1)  # To the left of 7

        # BILL button
        bill_btn = self.create_bill_button()
        layout.addWidget(bill_btn, 3, 0, 1, 1)  # To the left of +/-

    def create_action_button(self, text, style):
        """Create an action button"""
        btn = QPushButton(text)
        btn.setStyleSheet(style)
        btn.setFixedSize(ACTION_BUTTON_WIDTH, ACTION_BUTTON_HEIGHT)
        btn.clicked.connect(lambda: self.button_clicked(text))
        self.buttons[text] = btn
        return btn

    def create_bill_amount_display(self):
        """Create the bill amount display label"""
        bill_amount_label = QLabel("BILL AMOUNT\n0.00")
        bill_amount_label.setAlignment(Qt.AlignCenter)
        bill_amount_label.setFont(QFont("Arial", 10, QFont.Bold))
        bill_amount_label.setStyleSheet(ActionButtonStyles.BILL_AMOUNT_STYLE)
        bill_amount_label.setFixedSize(ACTION_BUTTON_WIDTH, BUTTON_SIZE)
        self.bill_amount_label = bill_amount_label  # Store reference for updates
        return bill_amount_label

    def create_bill_button(self):
        """Create the main BILL button"""
        bill_btn = QPushButton("BILL")
        bill_btn.setFont(QFont("Arial", 12, QFont.Bold))
        bill_btn.setStyleSheet(ActionButtonStyles.BILL_BUTTON_STYLE)
        bill_btn.setFixedSize(ACTION_BUTTON_WIDTH, BUTTON_SIZE)
        bill_btn.clicked.connect(self.process_bill)
        self.buttons["BILL"] = bill_btn
        return bill_btn

    def button_clicked(self, button_name):
        """Handle action button clicks"""
        print(f"Action button clicked: {button_name}")

        if button_name == "ADD ROW":
            self.add_new_row()
        elif button_name == "DELETE ROW":
            self.remove_selected_item()
        elif button_name == "PRICE":
            self.set_price_field()
        elif button_name == "QTY":
            self.set_qty_field()

    def add_new_row(self):
        """Add a new row to the billing list"""
        print(f"ADD ROW clicked - Current customer: {self.current_customer}")

        if self.billing_list is not None:
            # Add a new item with default values
            item_name = "New Item"
            qty = 1
            price = 5.00

            self.billing_list.add_item(item_name, qty, price)
            self.update_bill_amount()
            print(f"Added new item to {self.billing_list.get_current_customer()}: {item_name}")
        else:
            print("ERROR: Billing list not connected!")

    def remove_selected_item(self):
        """Delete the last row from the billing list"""
        if self.billing_list is not None:
            self.billing_list.remove_selected_item()
            self.update_bill_amount()
        else:
            print("ERROR: Billing list not connected!")

    def set_price_field(self):
        """Set the selected field to price for keypad input"""
        if self.billing_list and self.billing_list.selected_item_widget:
            item = self.billing_list.selected_item_widget
            self.billing_list.selected_field_name = "price"
            item.select_field("price")  # ✅ This will highlight the field
            if hasattr(self.billing_list, 'keypad') and self.billing_list.keypad:
                self.billing_list.keypad.reset_input()  # ✅ Clear buffer
            print(f"Field set to PRICE for selected item")
        else:
            print("No item selected for price editing")

    def set_qty_field(self):
        """Set the selected field to quantity for keypad input"""
        if self.billing_list and self.billing_list.selected_item_widget:
            item = self.billing_list.selected_item_widget
            self.billing_list.selected_field_name = "qty"
            item.select_field("qty")  # ✅ This will highlight the field
            if hasattr(self.billing_list, 'keypad') and self.billing_list.keypad:
                self.billing_list.keypad.reset_input()  # ✅ Clear buffer
            print(f"Field set to QTY for selected item")
        else:
            print("No item selected for quantity editing")

    def update_bill_amount(self):
        """Update the bill amount display"""
        if self.billing_list is not None and hasattr(self, 'bill_amount_label'):
            total = self.billing_list.get_current_customer_total()
            self.bill_amount_label.setText(f"BILL AMOUNT\n{total:.2f}")

    def process_bill(self):
        """Handle bill processing and print a receipt"""
        max_character = 46  # Maximum characters per line (adjustable for testing)

        if self.billing_list is not None:
            total = self.billing_list.get_current_customer_total()
            items = self.billing_list.get_current_customer_items()
            customer = self.billing_list.get_current_customer()

            # Format the receipt
            receipt_lines = []
            receipt_lines.append("RECEIPT".center(max_character, "-"))
            receipt_lines.append(f"Customer: {customer}".ljust(max_character))
            receipt_lines.append("-" * max_character)
            receipt_lines.append(f"{'No.':<4}{'Name':<16}{'Price':<8}{'Qty':<4}{'Amt':<8}")
            receipt_lines.append("-" * max_character)

            for idx, item in enumerate(items, start=1):
                name = item.item_name[:15]  # Truncate name to fit
                price = f"{item.price:.2f}"
                qty = f"{item.qty}"
                amount = f"{item.total():.2f}"
                receipt_lines.append(f"{idx:<4}{name:<16}{price:<8}{qty:<4}{amount:<8}")

            receipt_lines.append("-" * max_character)
            receipt_lines.append(f"{'TOTAL:':<32}{total:.2f}".rjust(max_character))
            receipt_lines.append("-" * max_character)

            # Join the receipt lines
            receipt_content = "\n".join(receipt_lines)

            # Print the receipt
            print("Printing receipt...")
            print(receipt_content)  # For debugging purposes

            try:
                if not self.printer_tester.is_printer_initialized():
                    self.printer_tester.run()  # Initialize the printer if not already done
                self.printer_tester.print_receipt(receipt_content)
            except Exception as e:
                print(f"❌ Failed to print receipt: {e}")
        else:
            print("No billing list connected!")