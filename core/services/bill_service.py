from database.bill_dao import BillDAO
from core.models.bill import Bill

class BillService:
    def __init__(self):
        self.dao = BillDAO()

    def clear_bill_items(self, bill_id: int) -> None:
        """
        Removes all items for the given bill and resets the total.
        """
        dao = self.dao
        cur = dao.conn.cursor()
        cur.execute("DELETE FROM bill_items WHERE bill_id = ?", (bill_id,))
        cur.execute("UPDATE bills SET total = 0 WHERE id = ?", (bill_id,))
        dao.conn.commit()

    def create_bill(self, customer_id: str) -> int:
        return self.dao.create_bill(customer_id)

    def add_item_to_bill(self, bill_id: int, product_id: int, qty: float, price: float) -> int:
        return self.dao.add_item(bill_id, product_id, qty, price)

    def get_bill(self, bill_id: int) -> Bill | None:
        return self.dao.get_bill(bill_id)

    def list_bills(self) -> list[Bill]:
        return self.dao.list_bills()

    def delete_bill(self, bill_id: int) -> bool:
        return self.dao.delete_bill(bill_id)

    def remove_item(self, item_id: int) -> bool:
        return self.dao.remove_item(item_id)

