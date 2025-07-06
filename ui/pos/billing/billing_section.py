from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QGridLayout, QPushButton, QHBoxLayout,
    QSizePolicy, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .billing_list import BillingList
from .keypad import Keypad
from .action_buttons import ActionButtons
from utils.styles import BillingStyles


class BillingSection:
    def __init__(self):
        self.keypad = Keypad()
        self.action_buttons = ActionButtons()
        self.billing_list = None
        self.customer_buttons = {}  # Store customer button references

    def create_billing_section(self):
        billing_frame = QFrame()
        billing_frame.setStyleSheet(BillingStyles.FRAME_STYLE)

        main_layout = QVBoxLayout(billing_frame)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        # Top: Customer selection buttons
        main_layout.addWidget(self._build_customer_section(), stretch=0)

        # Middle: Billing item list
        self.billing_list = BillingList()
        self.keypad.set_billing_list(self.billing_list)  # <-- now valid
        self.billing_list.set_keypad(self.keypad)

        self.billing_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.billing_list, stretch=1)

        # Bottom: Keypad + Action buttons
        keypad_area = self._build_keypad_area()
        main_layout.addWidget(keypad_area, stretch=0)

        # IMPORTANT: Connect the components AFTER creating them
        self.action_buttons.set_billing_list(self.billing_list)
        self.action_buttons.set_current_customer("C1")  # Set initial customer

        # Set initial customer selection (C1)
        self._update_customer_button_styles("C1")

        return billing_frame

    # --- UI Components ---

    def _build_customer_section(self):
        frame = QFrame()
        frame.setStyleSheet(BillingStyles.CUSTOMER_FRAME_STYLE)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        for index in range(1, 4):
            customer_id = f"C{index}"
            button = self._create_customer_button(customer_id)
            self.customer_buttons[customer_id] = button
            layout.addWidget(button)

        return frame

    def _create_customer_button(self, label):
        button = QPushButton(label)
        button.setCursor(Qt.PointingHandCursor)
        button.setFont(QFont("Arial", 14, QFont.Bold))
        button.setStyleSheet(BillingStyles.CUSTOMER_BUTTON_STYLE)
        button.setFixedHeight(50)
        # capture `product` in the lambda and call our handler
        button.clicked.connect(lambda _checked, p=label: self._on_customer_click(p))
        return button

    def _build_keypad_area(self):
        container = QWidget()
        layout = QGridLayout(container)
        layout.setSpacing(5)

        self.action_buttons.add_to_layout(layout)
        self.keypad.add_to_layout(layout)

        container.setLayout(layout)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        return container

    # --- Event Handlers ---

    def _on_customer_click(self, customer_name):
        """Handle customer button clicks"""
        print(f"Customer {customer_name} clicked")

        # Switch billing list to show selected customer's data
        if self.billing_list:
            self.billing_list.switch_customer(customer_name)

        # Update button styles to show selection
        self._update_customer_button_styles(customer_name)

        # IMPORTANT: Update action buttons to know current customer
        if self.action_buttons:
            self.action_buttons.set_current_customer(customer_name)
            self.action_buttons.update_bill_amount()  # Update bill amount display

    def _update_customer_button_styles(self, selected_customer):
        """Update customer button styles to show which is selected"""
        for customer_id, button in self.customer_buttons.items():
            if customer_id == selected_customer:
                # Selected customer button style
                button.setStyleSheet(BillingStyles.CUSTOMER_BUTTON_SELECTED_STYLE)
            else:
                # Normal customer button style
                button.setStyleSheet(BillingStyles.CUSTOMER_BUTTON_STYLE)