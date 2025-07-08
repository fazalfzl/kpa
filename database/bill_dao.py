from sqlite3 import Row
from datetime import datetime

from core.models.bill import Bill, BillItem
from .db_manager import DBManager


class BillDAO:
    def __init__(self, db_path: str = "pos.db"):
        self.conn = DBManager.get_instance(db_path).get_connection()

    def create_bill(self, customer_id:str, date:str=None) -> int:
        date = date or datetime.now().isoformat()
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO bills(customer_id,date) VALUES(?,?)",
            (customer_id, date),
        )
        self.conn.commit()
        return cur.lastrowid

    def add_item(self, bill_id:int, product_id:int, quantity:float, price:float) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO bill_items(bill_id,product_id,quantity,price) VALUES(?,?,?,?)",
            (bill_id, product_id, quantity, price),
        )
        # update bill total
        cur.execute(
            "UPDATE bills SET total = total + ? WHERE id = ?",
            (quantity * price, bill_id),
        )
        self.conn.commit()
        return cur.lastrowid

    def get_bill(self, bill_id:int) -> Bill|None:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM bills WHERE id=?", (bill_id,))
        row = cur.fetchone()
        if not row:
            return None
        bill = Bill(id=row["id"], customer_id=row["customer_id"], date=row["date"], total=row["total"])
        cur.execute("SELECT * FROM bill_items WHERE bill_id=?", (bill_id,))
        for r in cur.fetchall():
            bill.items.append(BillItem(r["id"], r["bill_id"], r["product_id"], r["quantity"], r["price"]))
        return bill

    def list_bills(self) -> list[Bill]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM bills ORDER BY date DESC")
        bills = []
        for r in cur.fetchall():
            b = Bill(r["id"], r["customer_id"], r["date"], r["total"])
            bills.append(b)
        return bills

    def remove_item(self, item_id:int) -> bool:
        cur = self.conn.cursor()
        # get item to adjust total
        cur.execute("SELECT bill_id, quantity, price FROM bill_items WHERE id=?", (item_id,))
        item = cur.fetchone()
        if not item:
            return False
        cur.execute(
            "UPDATE bills SET total = total - ? WHERE id = ?",
            (item["quantity"] * item["price"], item["bill_id"]),
        )
        cur.execute("DELETE FROM bill_items WHERE id=?", (item_id,))
        self.conn.commit()
        return True

    def delete_bill(self, bill_id:int) -> bool:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM bill_items WHERE bill_id=?", (bill_id,))
        cur.execute("DELETE FROM bills WHERE id=?", (bill_id,))
        self.conn.commit()
        return True