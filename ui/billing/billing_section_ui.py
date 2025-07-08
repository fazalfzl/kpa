from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ..utils.styles import BillingStyles


class BillingSectionUI:
    def __init__(self, logic):
        self.logic = logic

    def create_ui(self):
        billing_frame = QFrame()
        billing_frame.setStyleSheet(BillingStyles.FRAME_STYLE)

        main_layout = QVBoxLayout(billing_frame)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        self._add_editing_label(main_layout)
        self._add_save_cancel_buttons(main_layout)
        main_layout.addWidget(self._build_customer_section(), stretch=0)
        self._add_billing_list(main_layout)
        main_layout.addWidget(self._build_keypad_area(), stretch=0)

        return billing_frame

    def _add_editing_label(self, layout):
        self.logic.editing_bill_label = QLabel("")
        self.logic.editing_bill_label.setStyleSheet(BillingStyles.EDITING_BILL_LABEL_STYLE)
        self.logic.editing_bill_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logic.editing_bill_label, stretch=0)

    def _add_save_cancel_buttons(self, layout):
        save_cancel_layout = QHBoxLayout()
        self.logic.save_button = QPushButton("Save")
        self.logic.save_button.clicked.connect(self.logic._save_changes)
        self.logic.cancel_button = QPushButton("Cancel")
        self.logic.cancel_button.clicked.connect(self.logic._cancel_changes)
        save_cancel_layout.addWidget(self.logic.save_button)
        save_cancel_layout.addWidget(self.logic.cancel_button)
        layout.addLayout(save_cancel_layout)
        self.logic._toggle_editing_ui(False)

    def _build_customer_section(self):
        customer_frame = QFrame()
        customer_frame.setStyleSheet(BillingStyles.CUSTOMER_FRAME_STYLE)
        layout = QGridLayout(customer_frame)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        for i in range(1, 4):
            customer_id = f"C{i}"
            button = QPushButton(customer_id)
            button.setStyleSheet(BillingStyles.CUSTOMER_BUTTON_STYLE)
            button.setFont(QFont("Arial", 10, QFont.Bold))
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda _, cid=customer_id: self.logic._on_customer_click(cid))
            layout.addWidget(button, 0, i - 1)
            self.logic.customer_buttons[customer_id] = button

        return customer_frame

    def _add_billing_list(self, layout):
        self.logic.billing_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.logic.billing_list, stretch=1)

    def _build_keypad_area(self):
        keypad_frame = QFrame()
        layout = QGridLayout(keypad_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.logic.keypad.add_to_layout(layout)
        self.logic.action_buttons_ui.add_to_layout(layout)

        return keypad_frame
