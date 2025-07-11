from PyQt5.QtWidgets import QPushButton, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.billing.action_buttons.logic import ActionButtonsLogic
from ui.utils.styles import ActionButtonStyles, GlobalStyles, WeightButtonStyles
from utils.constants import ACTION_BUTTON_WIDTH, ACTION_BUTTON_HEIGHT, BUTTON_SIZE
from PyQt5.QtWidgets import QLineEdit

class ActionButtonsUI:
    def __init__(self, logic: ActionButtonsLogic, update_label_cb):
        self.logic = logic
        self.update_label_cb = update_label_cb  # or directly set label here

        self.buttons = {}
        self.weight_button = None
        self.bill_amount_label = None

        # self.barcode_input = None  # Add this

    def set_billing_section(self, billing_section):
        self.logic.set_billing_section(billing_section)

    def set_billing_list(self, billing_list):
        self.logic.set_billing_list(billing_list)

    def set_current_customer(self, customer_id):
        self.logic.set_current_customer(customer_id)

    def add_to_layout(self, layout):
        if not isinstance(layout, QGridLayout):
            raise TypeError("Layout must be QGridLayout")

        layout.addWidget(
            self._create_action_button("ROW +", self.logic.add_new_row, ActionButtonStyles.ADD_ROW_STYLE), 0, 0)
        layout.addWidget(self._create_action_button("ROW -", self.logic.remove_selected_item,
                                                    ActionButtonStyles.DELETE_ROW_STYLE), 1, 0)
        layout.addWidget(
            self._create_action_button("PRICE", self.logic.set_price_field, ActionButtonStyles.PRICE_STYLE), 1, 4)
        layout.addWidget(self._create_action_button("QTY", self.logic.set_qty_field, ActionButtonStyles.QTY_STYLE), 0,
                         4)

        self.weight_button = self._create_weight_button()
        self.logic.weight_button = self.weight_button
        self.weight_button.clicked.connect(self.logic.on_weight_button_clicked)

        layout.addWidget(self.weight_button, 2, 4)

        layout.addWidget(self.weight_button, 2, 4)

        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Scan Barcode")
        layout.addWidget(self.barcode_input, 3, 4)  # Adjust row as needed


        self.bill_amount_label = self._create_bill_amount_display()
        self.logic.bill_amount_label = self.bill_amount_label
        layout.addWidget(self.bill_amount_label, 2, 0)

        layout.addWidget(
            self._create_action_button("BILL", self.logic.process_bill, ActionButtonStyles.BILL_BUTTON_STYLE, True), 3,
            0)

    def _create_action_button(self, text, handler, style, large_font=False):
        btn = QPushButton(text)
        font = QFont("Arial", 12 if large_font else 10, QFont.Bold)
        btn.setFont(font)
        btn.setStyleSheet(style)
        btn.setFixedSize(ACTION_BUTTON_WIDTH, BUTTON_SIZE if large_font else ACTION_BUTTON_HEIGHT)
        btn.clicked.connect(handler)
        self.buttons[text] = btn
        return btn

    def _create_weight_button(self):
        btn = QPushButton("Weight: 0.00 kg")
        btn.setFont(QFont("Arial", 10, QFont.Bold))
        btn.setStyleSheet(WeightButtonStyles.BUTTON_STYLE )
        btn.setFixedSize(ACTION_BUTTON_WIDTH, BUTTON_SIZE)
        return btn

    def _create_bill_amount_display(self):
        label = QLabel("0.00")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 10, QFont.Bold))
        label.setStyleSheet(ActionButtonStyles.BILL_AMOUNT_STYLE)
        label.setFixedSize(ACTION_BUTTON_WIDTH, BUTTON_SIZE)
        return label
