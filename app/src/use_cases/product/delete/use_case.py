from typing import Optional

from app.src.exceptions import (
  ProductNotFoundException,
  ProductRepositoryException,
  ProductBusinessException,
)

from app.src.core.models import Product
from app.src.repositories import ProductRepository
from .request import DeleteProductRequest
from .response import DeleteProductResponse



class DeleteProduct:
  def __init__(self, product_repository: ProductRepository) -> None:
    self.product_repository = product_repository
  
  def __call__(self, request: DeleteProductRequest)-> Optional[DeleteProductResponse]:
    try:
      existing_product = self.product_repository.get_by_id(request.product_id)
      if not existing_product:
          raise ProductNotFoundException(product_id=request.product_id)
      response = self.product_repository.delete(existing_product.product_id)
      return  DeleteProductResponse(response)
    except ProductRepositoryException as e:
      raise ProductBusinessException(str(e))
