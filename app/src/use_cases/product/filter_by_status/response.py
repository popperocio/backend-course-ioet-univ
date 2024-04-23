from decimal import Decimal

from typing import List, NamedTuple

from ....core.models._product import Product


class FilterProductsByStatusResponse(NamedTuple):
   products: List[Product]
