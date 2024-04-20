from typing import Optional

from app.src.exceptions import (
  ProductNotFoundException,
  ProductRepositoryException
)

from app.src.core.models import Product
from app.src.repositories import ProductRepository

from .request import EditProductRequest
from .response import EditProductResponse



class EditProduct:
  def __init__(self, product_repository: ProductRepository) -> None:
    self.product_repository = product_repository
  
  def __call__(self, request: EditProductRequest)-> Optional[EditProductResponse]:
    try:
      product_to_edit = self.product_repository.get_by_id(request.product_id)
      if not product_to_edit:
          raise ProductNotFoundException(product_id=request.product_id)
      updated_product = Product(**request._asdict())
      response = self.product_repository.edit(updated_product)
      if not response:
        pass
      return  EditProductResponse(**response._asdict())
    except ProductRepositoryException as e:
      pass
