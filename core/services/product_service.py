from core.models.product import Product
from database.product_repository import ProductRepository


class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    def create_product(self, **kwargs) -> int:
        return self.repo.create(**kwargs)

    def update_product(self, product_id: int, **kwargs) -> bool:
        return self.repo.update(product_id, **kwargs)

    def delete_product_by_name(self, name: str) -> bool:
        return self.repo.delete_by_name(name)

    def get_all(self) -> list[Product]:
        return self.repo.get_all()

    def get_by_barcode(self, barcode: str) -> Product | None:
        return self.repo.get_by_barcode(barcode)

    def get_by_id(self, id: int) -> Product | None:
        return self.repo.get_by_id(id)

    def get_by_name(self, name: str) -> Product | None:
        return self.repo.get_by_name(name)

    def get_by_category(self, category):
        result = self.repo.get_by_category(category)  # or however it's implemented
        return result if result is not None else []

    def reorder_products(self, id1: int, id2: int):
        self.repo.swap_order(id1, id2)
