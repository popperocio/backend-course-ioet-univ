from decimal import Decimal
from typing import Callable
from unittest.mock import Mock

import pytest
from app.src.use_cases import (
    FilterProductsByStatus, 
    FilterProductsByStatusResponse,
    FilterProductsByStatusRequest, 
    CreateProduct, 
    CreateProductRequest)
from factories import memory_product_repository
from app.src.exceptions import ProductNoneException

class TestFilterProductsByStatusProductUseCase:
    
    def test__filter_product_by_status_returns_list_of_products_when_successful(
        self, 
        products_factory: Callable
    ):
        products = products_factory(3)
        product_memory_repository = memory_product_repository()
        create_product_use_case = CreateProduct(product_memory_repository)
        for product in products:
            product_to_create =  CreateProductRequest(
            product_id=product.product_id,
            user_id=product.user_id,
            name=product.name,
            description=product.description,
            price=product.price,
            location=product.location,
            status=product.status,
            is_available=product.is_available,      
            )
            create_product_use_case(product_to_create)
        filter_by_status_request = FilterProductsByStatusRequest(
            status = "Used",
        )
        filter_product__by_status_use_case = FilterProductsByStatus(
            product_memory_repository)
        response = filter_product__by_status_use_case(filter_by_status_request)
        assert isinstance(response,FilterProductsByStatusResponse)


    def test_should_raise_business_exception_on_repository_exception(self,):
        product_memory_repository = memory_product_repository()
        filter_products_by_status_product_use_case = FilterProductsByStatus(
            product_memory_repository)
        product_memory_repository.filter_products_by_status = Mock(return_value=None)
        filter_products_by_status_request = FilterProductsByStatusRequest(
            status="new",
        )
        expected_exception = ProductNoneException()
        
        with pytest.raises(ProductNoneException) as captured_exception:
            filter_products_by_status_product_use_case(filter_products_by_status_request)

        assert str(captured_exception.value) == "The Product is None."
        assert isinstance(captured_exception.value, type(expected_exception))