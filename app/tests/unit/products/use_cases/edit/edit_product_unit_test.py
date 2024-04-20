from decimal import Decimal
from app.src.use_cases import (EditProduct, EditProductRequest, EditProductResponse, CreateProduct, CreateProductRequest)
from factories import memory_product_repository


class TestEditProductUseCase:
    
    def test__edit_product_returns_product_updated_when_successful(self, product_factory):
        product = product_factory()
        product_memory_repository = memory_product_repository()
        create_product_use_case = CreateProduct(product_memory_repository)
        product_to_create = CreateProductRequest(
            product_id = product.product_id,
            user_id = product.user_id,
            name = product.name,
            description = product.description,
            price = product.price,
            location = product.location,
            status = product.status,
            is_available = product.is_available
        )
        create_product_use_case(product_to_create)
        edit_request = EditProductRequest(
            product_id = product.product_id,
            user_id = product.user_id,
            name = product.name,
            description = product.description,
            price = product.price,
            location = product.location,
            status = product.status,
            is_available = False
        )
        edit_product_use_case = EditProduct(product_memory_repository)
        response = edit_product_use_case(edit_request)
        assert isinstance(response, EditProductResponse)
        assert response.is_available == False


