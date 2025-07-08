from core.services.bill_service import BillService
from core.services.product_service import ProductService
from ui.billing.action_buttons.logic import ActionButtonsLogic
from ui.billing.action_buttons.ui import ActionButtonsUI
from ui.billing.billing_list.ui import BillingListWidget
from ui.billing.keypad.logic import BillingKeypad
from ui.billing.section.ui import BillingSectionUI
from ui.utils.styles import BillingStyles
from ui.utils.ui_helpers import toggle_visibility

from utils.logger import get_logger
log = get_logger(__name__)


class BillingSection:
    def __init__(self, title_bar_logic=None):
        self.title_bar_logic = title_bar_logic
        # Core components
        self.billing_list = BillingListWidget()
        self.keypad = BillingKeypad()
        self.action_buttons_logic = ActionButtonsLogic()
        self.action_buttons_ui = ActionButtonsUI(self.action_buttons_logic, self._update_total_label)

        # Logic state
        self.customer_buttons = {}
        self.editing_bill_label = None
        self.current_editing_bill = None
        self.save_button = None
        self.cancel_button = None

        # Setup callbacks and shared objects
        self.action_buttons_logic.set_total_updater(self._update_total_label)
        self.action_buttons_logic.set_printer(self._get_printer_instance())

        # Wire component dependencies
        self._wire_components()

        # Build UI using references
        self.ui_builder = BillingSectionUI(self)



    def _wire_components(self):
        self.keypad.set_billing_list(self.billing_list)
        self.billing_list.set_keypad(self.keypad)
        self.action_buttons_logic.set_billing_list(self.billing_list)
        self.action_buttons_logic.set_billing_section(self)
        self.billing_list.action_buttons_logic = self.action_buttons_logic

        self.billing_list.logic.bill_changed.connect(self.action_buttons_logic.update_bill_amount)

    def _get_printer_instance(self):
        # Lazy init to avoid duplicate instances
        if not hasattr(self, '_printer_instance'):
            from utils.print_pkg.printer_config import PrinterTester
            self._printer_instance = PrinterTester()
        return self._printer_instance

    def create_billing_section(self):
        return self.ui_builder.create_ui()

    # --- Logic ---
    def _toggle_editing_ui(self, visible):
        toggle_visibility([self.editing_bill_label, self.save_button, self.cancel_button], visible)

    def _save_changes(self):
        if self.current_editing_bill:
            self.action_buttons_logic.process_bill()
            self.current_editing_bill = None
            self.editing_bill_label.setText("")
            self._toggle_editing_ui(False)

        # 🔁 Refresh title bar bill buttons
        if self.title_bar_logic:
            self.title_bar_logic.refresh_last_bills()

    def _cancel_changes(self):
        self.billing_list.clear_current_customer()
        self.current_editing_bill = None
        self.editing_bill_label.setText("")
        self._toggle_editing_ui(False)

    def load_bill(self, bill_id):
        bill_service = BillService()
        bill = bill_service.get_bill(bill_id)
        if not bill:
            log.info(f"Bill {bill_id} not found!")
            return

        self.billing_list.clear_current_customer()
        product_service = ProductService()
        for item in bill.items:
            product = product_service.get_by_id(item.product_id)
            if product:
                self.billing_list.add_item(product.name, item.quantity, item.price)

        self.current_editing_bill = bill_id
        self.editing_bill_label.setText(f"Editing Bill {bill_id}")
        self._toggle_editing_ui(True)

    # --- Event Handlers ---
    def _on_customer_click(self, customer_name):
        log.info(f"Customer {customer_name} clicked")
        self._switch_to_customer(customer_name)
        self._highlight_selected_customer(customer_name)
        self._update_action_buttons(customer_name)

    def _switch_to_customer(self, customer_name):
        if self.billing_list:
            self.billing_list.switch_customer(customer_name)

    def _highlight_selected_customer(self, customer_name):
        self._update_customer_button_styles(customer_name)

    def _update_customer_button_styles(self, selected_customer):
        for customer_id, button in self.customer_buttons.items():
            if customer_id == selected_customer:
                button.setStyleSheet(BillingStyles.CUSTOMER_BUTTON_SELECTED_STYLE)
            else:
                button.setStyleSheet(BillingStyles.CUSTOMER_BUTTON_STYLE)

    def _update_action_buttons(self, customer_name):
        if self.action_buttons_logic:
            self.action_buttons_logic.set_current_customer(customer_name)
            self.action_buttons_logic.update_bill_amount()

    def _update_total_label(self, total_text):
        if hasattr(self.action_buttons_ui, 'bill_amount_label'):
            self.action_buttons_ui.bill_amount_label.setText(total_text)