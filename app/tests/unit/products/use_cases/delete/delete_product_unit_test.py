from decimal import Decimal
from typing import Callable
from unittest.mock import Mock

import pytest
from app.src.use_cases import (DeleteProduct, DeleteProductRequest, DeleteProductResponse, CreateProduct, CreateProductRequest)
from factories import memory_product_repository
from app.src.exceptions import ProductNotFoundException, ProductNoneException, ProductBusinessException

class TestDeleteProductUseCase:
    
    def test__delete_product_returns_product_id_of_deleted_product_when_successful(
        self, 
        product_factory: Callable
    ):
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
        delete_request = DeleteProductRequest(
            product_id = product.product_id,
        )
        delete_product_use_case = DeleteProduct(product_memory_repository)
        response = delete_product_use_case(delete_request)
        assert isinstance(response, DeleteProductResponse)


    def test_delete_product_returns_a_not_found_exception_when_product_to_delete_is_not_found(
        self, 
    ):
        product_id = "8091"
        product_memory_repository = memory_product_repository()
        delete_request = DeleteProductRequest(product_id)
        delete_product_use_case = DeleteProduct(product_memory_repository)
        expected_exception = ProductNotFoundException(product_id)
        message_exception = f"The Product with the id '{product_id}' does not exist."

        with pytest.raises(ProductNotFoundException) as captured_exception:
            delete_product_use_case(delete_request)

        assert type(captured_exception.value) is type(expected_exception)
        assert message_exception == str(captured_exception.value)
        
    def test_delete_product_returns_business_exception_when_there_is_an_error_while_processing(
        self,
        product_factory
    ):
        product = product_factory()
        product_memory_repository = memory_product_repository()
        delete_product_use_case = DeleteProduct(product_memory_repository)
        product_memory_repository.get_by_id = Mock(
            side_effect=ProductBusinessException(
                "An error occurred while processing the request.")
            )
        delete_request = DeleteProductRequest(
            product_id=product.product_id,
        )
        expected_exception = ProductBusinessException()
        message_exception = "An error occurred while processing the request."

        with pytest.raises(ProductBusinessException) as captured_exception:
            delete_product_use_case(delete_request)

        assert str(captured_exception.value) == message_exception
        assert isinstance(captured_exception.value, type(expected_exception))