from decimal import Decimal
from typing import Any, Callable, List
from pytest import fixture
from faker import Faker
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


fake = Faker()

@fixture
def products_factory() -> Callable:
    def _factory(count: int = 4) -> List[Product]:
        products = []
        for _ in range(count):
            product = Product(
                product_id=fake.uuid4(),
                user_id=str(fake.random_number(digits=5)),
                name=fake.word(),
                description=fake.sentence(),
                price=Decimal(fake.random_number(4, True) / 100),
                location=fake.city(),
                status=fake.random_element(elements=[status.value for status in ProductStatuses]),
                is_available=fake.boolean()
            )
            products.append(product)
        return products

    return _factory