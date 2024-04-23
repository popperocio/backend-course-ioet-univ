from typing import NamedTuple

from ....core import ProductStatuses


class FilterProductsByStatusRequest(NamedTuple):
  status: ProductStatuses

