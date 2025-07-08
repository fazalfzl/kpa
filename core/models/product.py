class Product:
    def __init__(
        self,
        id: int,
        name: str,
        price: float,
        barcode: str,
        unit: str,
        image_path: str,
        order_index: int,
        category: str,
    ):
        self.id = id
        self.name = name
        self.price = price
        self.barcode = barcode
        self.unit = unit
        self.image_path = image_path
        self.order_index = order_index
        self.category = category
