from decimal import Decimal
from typing import Any, Callable
from pytest import fixture

from app.src.core import Product, ProductStatuses

@fixture
def product_factory() -> Callable:
    def _factory(**kwargs: Any) -> Product:
        return Product(
                 product_id="20",
                    user_id="1",
                    name="Headphones",
                    description="Noise cancellation",
                    price=Decimal(10.5),
                    location="Quito",
                    status=ProductStatuses.USED,
                    is_available=True,      
        )
    return _factory
