from PyQt5.QtWidgets import QPushButton
from utils.constants import BUTTON_SIZE
from ..utils.styles import BillingKeypadStyles

class BillingKeypadUI:
    def __init__(self, logic):
        self.logic = logic
        self.buttons = {}

    def add_buttons_to(self, layout):
        nums = [(1, 0, 1), (2, 0, 2), (3, 0, 3), (4, 1, 1), (5, 1, 2), (6, 1, 3),
                (7, 2, 1), (8, 2, 2), (9, 2, 3), (0, 3, 2)]
        for num, row, col in nums:
            btn = self._create_number_button(num)
            layout.addWidget(btn, row, col)

        layout.addWidget(self._create_op_button(".", BillingKeypadStyles.PLUS_MINUS_STYLE), 3, 1)
        layout.addWidget(self._create_op_button("X", BillingKeypadStyles.CLEAR_STYLE), 3, 3)

    def _create_number_button(self, num):
        btn = QPushButton(str(num))
        btn.setStyleSheet(BillingKeypadStyles.NUMBER_STYLE)
        btn.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        btn.clicked.connect(lambda: self.logic.number_clicked(num))
        self.buttons[str(num)] = btn
        return btn

    def _create_op_button(self, symbol, style):
        btn = QPushButton(symbol)
        btn.setStyleSheet(style)
        btn.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        btn.clicked.connect(lambda: self.logic.button_clicked(symbol))
        self.buttons[symbol] = btn
        return btn