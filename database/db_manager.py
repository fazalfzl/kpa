import sqlite3
from sqlite3 import Connection
import threading

class DBManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self, db_path: str = "pos.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    @classmethod
    def get_instance(cls, db_path: str = "pos.db"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(db_path)
        return cls._instance

    def _init_schema(self):
        cursor = self.conn.cursor()
        # products table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            price         REAL    NOT NULL,
            barcode       TEXT    UNIQUE,
            unit          TEXT,
            image_path    TEXT,
            order_index   INTEGER NOT NULL DEFAULT 0
        )""")
        # ensure order_index exists
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN order_index INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        cursor.execute("UPDATE products SET order_index = id WHERE order_index = 0")

        # <<< NEW: category column, default 'manual' >>>
        try:
            cursor.execute(
                "ALTER TABLE products ADD COLUMN category TEXT NOT NULL DEFAULT 'manual'"
            )
        except sqlite3.OperationalError:
            # already added
            pass

        # bills & items
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            date        TEXT,
            total       REAL    DEFAULT 0
        )""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bill_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id     INTEGER NOT NULL,
            product_id  INTEGER NOT NULL,
            quantity    REAL    NOT NULL,
            price       REAL    NOT NULL,
            FOREIGN KEY(bill_id) REFERENCES bills(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )""")
        self.conn.commit()

    def get_connection(self) -> Connection:
        return self.conn

    def close(self):
        self.conn.close()
        DBManager._instance = None