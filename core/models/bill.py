class BillItem:
    def __init__(self, id: int, bill_id: int, product_id: int, quantity: float, price: float):
        self.id = id
        self.bill_id = bill_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

class Bill:
    def __init__(self, id: int, customer_id: str, date: str, total: float):
        self.id = id
        self.customer_id = customer_id
        self.date = date
        self.total = total
        self.items: list[BillItem] = []
