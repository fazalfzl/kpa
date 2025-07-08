from sqlite3 import Row

from core.models.product import Product
from .db_manager import DBManager

class ProductRepository:
    def __init__(self, db_path: str = "pos.db"):
        self.conn = DBManager.get_instance(db_path).get_connection()

    def create(
        self,
        name: str,
        price: float,
        barcode: str,
        unit: str,
        image_path: str,
        category: str = "manual"
    ) -> int:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO products
              (name, price, barcode, unit, image_path, category)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, price, barcode or None, unit, image_path or None, category),
        )
        new_id = cur.lastrowid
        cur.execute("UPDATE products SET order_index = ? WHERE id = ?", (new_id, new_id))
        self.conn.commit()
        return new_id

    def get_all(self) -> list[Product]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products ORDER BY order_index, name")
        rows = cur.fetchall()
        return [self._row_to_obj(r) for r in rows]

    def get_by_category(self, category: str) -> list[Product]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM products WHERE category = ? ORDER BY order_index, name",
            (category,),
        )
        rows = cur.fetchall()
        return [self._row_to_obj(r) for r in rows]

    def get_by_barcode(self, barcode: str) -> Product | None:
        """Get product by barcode for scanning functionality"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products WHERE barcode = ?", (barcode,))
        row = cur.fetchone()
        return self._row_to_obj(row) if row else None

    def get_by_id(self, id: int) -> Product | None:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products WHERE id = ?", (id,))
        row = cur.fetchone()
        return self._row_to_obj(row) if row else None

    def update(self, id: int, **fields) -> bool:
        allowed = {"name", "price", "barcode", "unit", "image_path", "order_index", "category"}
        setters = ", ".join(f"{k}=?" for k in fields if k in allowed)
        params = [fields[k] for k in fields if k in allowed] + [id]
        if not setters:
            return False
        self.conn.cursor().execute(f"UPDATE products SET {setters} WHERE id = ?", params)
        self.conn.commit()
        return True

    def delete(self, id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM products WHERE id = ?", (id,))
        self.conn.commit()
        return cur.rowcount > 0

    def swap_order(self, id1: int, id2: int) -> None:
        cur = self.conn.cursor()
        cur.execute("SELECT order_index FROM products WHERE id = ?", (id1,))
        o1 = cur.fetchone()["order_index"]
        cur.execute("SELECT order_index FROM products WHERE id = ?", (id2,))
        o2 = cur.fetchone()["order_index"]
        cur.execute("UPDATE products SET order_index = ? WHERE id = ?", (o2, id1))
        cur.execute("UPDATE products SET order_index = ? WHERE id = ?", (o1, id2))
        self.conn.commit()

    def _row_to_obj(self, row: Row) -> Product:
        return Product(
            id = row["id"],
            name = row["name"],
            price = row["price"],
            barcode = row["barcode"],
            unit = row["unit"],
            image_path = row["image_path"],
            order_index = row["order_index"],
            category = row["category"],
        )

    def get_by_name(self, name) -> Product | None:
        """Get product by name, useful for editing"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products WHERE name = ?", (name,))
        row = cur.fetchone()
        return self._row_to_obj(row) if row else None

    def delete_by_name(self, name ) -> bool:
        """Delete product by name, useful for editing"""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM products WHERE name = ?", (name,))
        self.conn.commit()
        return cur.rowcount > 0