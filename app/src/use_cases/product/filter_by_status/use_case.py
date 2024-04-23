from typing import Optional

from app.src.exceptions import (
  ProductRepositoryException,
  ProductBusinessException,
  ProductNoneException
)

from app.src.repositories import ProductRepository
from .request import FilterProductsByStatusRequest
from .response import FilterProductsByStatusResponse

class FilterProductsByStatus:
  def __init__(self, product_repository: ProductRepository) -> None:
    self.product_repository = product_repository
  
  def __call__(self, request: FilterProductsByStatusRequest)-> Optional[FilterProductsByStatusResponse]:
    try:
      response = self.product_repository.filter_products_by_status(request.status)
      if response is None:
        raise ProductNoneException()
      return  FilterProductsByStatusResponse(response)
    except ProductRepositoryException as e:
      raise ProductBusinessException(str(e))
