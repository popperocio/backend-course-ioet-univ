from typing import List, Optional
from app.src import ProductRepository, ProductRepositoryException, Product

class MemoryProductRepository(ProductRepository):
  products: List[Product]

  def __init__(self) -> None:
    self.products = []

  def list_all(self) -> List[Product]:
    try:
      return self.products
    except ProductRepositoryException:
      raise ProductRepositoryException(method="list")

  def create(self, product: Product) -> Product:
    try:
      self.products.append(product)
      return product
    except Exception:
      raise ProductRepositoryException(method="create")

  def get_by_id(self, product_id: str) -> Optional[Product]:
    try:
      return next(
        (product for product in self.products if product.product_id == product_id),
        None,
      )
    except Exception:
      raise ProductRepositoryException(method="find")

  def edit(self, product_to_edit: Product) -> Product:
    try:
      for product in self.products:
        if product.product_id == product_to_edit.product_id:
          self.products.append(product_to_edit)
          self.products.remove(product)
          return product_to_edit
        return None
    except Exception:
      raise ProductRepositoryException(method="edit")

  def delete(self, product_id: str) -> Product:
    try:
      existing_product = self.get_by_id(product_id=product_id)
      if existing_product:
          self.products.remove(existing_product)
          return product_id
    except Exception:
      raise ProductRepositoryException(method="delete")
    
  def filter_products_by_status(self, status:str) -> List[Product]:
    filtered_products = []
    try:
      for product in self.products:
        if product.status == status:
          filtered_products.append(product)
      return filtered_products
    except Exception:
      raise ProductRepositoryException(method="filter products by status")