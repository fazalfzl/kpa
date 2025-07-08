from database.bill_dao import BillDAO
from database.product_repository import ProductRepository
from utils.print_pkg.printer_config import PrinterTester

class ActionButtonsLogic:
    def __init__(self):
        self.billing_list = None
        self.current_customer = "C1"
        self.billing_section = None
        self.printer_tester = PrinterTester()

        self._update_total_label = lambda val: None  # safe no-op
        self._printer = None

    def set_billing_list(self, billing_list):
        self.billing_list = billing_list

    def set_billing_section(self, billing_section):
        self.billing_section = billing_section

    def set_current_customer(self, customer_id):
        self.current_customer = customer_id

    def add_new_row(self):
        if not self.billing_list:
            return
        self.billing_list.add_item("New Item", 1, 5.00)
        self.update_bill_amount()

    def remove_selected_item(self):
        if not self.billing_list:
            return
        self.billing_list.remove_selected_item()
        self.update_bill_amount()

    def set_price_field(self):
        if self.billing_list and self.billing_list.selected_item_widget:
            item = self.billing_list.selected_item_widget
            self.billing_list.selected_field_name = "price"
            item.select_field("price")
            if hasattr(self.billing_list, 'keypad') and self.billing_list.keypad:
                self.billing_list.keypad.reset_input()

    def set_qty_field(self):
        if self.billing_list and self.billing_list.selected_item_widget:
            item = self.billing_list.selected_item_widget
            self.billing_list.selected_field_name = "qty"
            item.select_field("qty")
            if hasattr(self.billing_list, 'keypad') and self.billing_list.keypad:
                self.billing_list.keypad.reset_input()


    def process_bill(self):
        if not self.billing_list:
            return

        total = self.billing_list.get_current_customer_total()
        items = self.billing_list.get_current_customer_items()
        customer = self.billing_list.get_current_customer()
        bill_dao = BillDAO()

        if self.billing_section and self.billing_section.current_editing_bill:
            bill_id = self.billing_section.current_editing_bill
            cur = bill_dao.conn.cursor()
            # Delete old items and reset total
            cur.execute("DELETE FROM bill_items WHERE bill_id = ?", (bill_id,))
            cur.execute("UPDATE bills SET total = 0 WHERE id = ?", (bill_id,))

        else:
            bill_id = bill_dao.create_bill(customer_id=customer)

        for item in items:
            product = ProductRepository().get_by_name(item.item_name)
            if product:
                bill_dao.add_item(bill_id, product.id, item.qty, item.price)

        self.billing_list.clear_current_customer()

        if self.billing_section:
            self.billing_section.current_editing_bill = None
            self.billing_section.editing_bill_label.setText("")

        receipt_lines = []
        max_character = 48
        max_name_length = 22
        max_price_length = 7
        max_qty_length = 7
        max_amt_length = 7

        receipt_lines.append("-" * max_character)
        receipt_lines.append(
            f"{'No.':<4}{'Name':<{max_name_length}}{'Price':<{max_price_length}}"
            f"{'Qty':<{max_qty_length}}{'Amt':<{max_amt_length}}")
        receipt_lines.append("-" * max_character)

        for idx, item in enumerate(items, start=1):
            name = item.item_name[:max_name_length]
            price = f"{item.price:.2f}"[:max_price_length]
            qty = f"{item.qty}"[:max_qty_length]
            amount = f"{item.total():.2f}"[:max_amt_length]
            receipt_lines.append(
                f"{idx:<4}{name:<{max_name_length}}{price:<{max_price_length}}"
                f"{qty:<{max_qty_length}}{amount:<{max_amt_length}}")

        receipt_lines.append("-" * max_character)
        receipt_content = "\n".join(receipt_lines)

        try:
            if not self.printer_tester.is_printer_initialized():
                self.printer_tester.run()
            self.printer_tester.print_receipt(receipt_content, total=total)
        except Exception as e:
            print(f"Failed to print receipt: {e}")

        # 🔁 Refresh title bar buttons after new bill is created
        if self.billing_section and self.billing_section.title_bar_logic:
            self.billing_section.title_bar_logic.refresh_last_bills()

    def set_total_updater(self, callback):
        self._update_total_label = callback


    def update_bill_amount(self):
        if self.billing_list and hasattr(self, 'bill_amount_label'):
            total = self.billing_list.get_current_customer_total()
            self._update_total_label(f"BILL AMOUNT\n{total:.2f}")

    def set_printer(self, printer):
        self._printer = printer
