from decimal import Decimal
from typing import Callable
from unittest.mock import Mock

import pytest
from app.src.use_cases import (EditProduct, EditProductRequest, EditProductResponse, CreateProduct, CreateProductRequest)
from factories import memory_product_repository
from app.src.exceptions import ProductNotFoundException, ProductNoneException, ProductBusinessException

class TestEditProductUseCase:
    
    def test__edit_product_returns_product_updated_when_successful(
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


    def test_should_return_an_exception_when_product_to_update_is_not_found(
        self, 
        product_factory: Callable
    ):
        product = product_factory()
        product_memory_repository = memory_product_repository()
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
       
        expected_exception = ProductNotFoundException(product.product_id)
        message_exception = f"The Product with the id '{product.product_id}' does not exist."

        with pytest.raises(ProductNotFoundException) as captured_exception:
            edit_product_use_case(edit_request)

        assert type(captured_exception.value) is type(expected_exception)
        assert message_exception == str(captured_exception.value)
   
    def test_should_return_exception_when_edit_returns_none(self,product_factory):
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
            product_id=product.product_id,
            user_id=product.user_id,
            name=product.name,
            description=product.description,
            price=product.price,
            location=product.location,
            status=product.status,
            is_available=False
        )
        product_memory_repository.edit = lambda product: None
        edit_product_use_case = EditProduct(product_memory_repository)
        expected_exception = ProductNoneException()
        message_exception = "The Product is None."

        with pytest.raises(ProductNoneException) as captured_exception:
            edit_product_use_case(edit_request)

        assert isinstance(captured_exception.value, type(expected_exception))
        assert str(captured_exception.value) == message_exception
        
    def test_should_raise_business_exception_on_repository_exception(self,product_factory):
        product = product_factory()
        product_memory_repository = memory_product_repository()
        edit_product_use_case = EditProduct(product_memory_repository)
        product_memory_repository.get_by_id = Mock(
            side_effect=ProductBusinessException(
                "An error occurred while processing the request.")
            )
        edit_request = EditProductRequest(
            product_id=product.product_id,
            user_id=product.user_id,
            name=product.name,
            description=product.description,
            price=product.price,
            location=product.location,
            status=product.status,
            is_available=False
        )
        expected_exception = ProductBusinessException()
        message_exception = "An error occurred while processing the request."

        with pytest.raises(ProductBusinessException) as captured_exception:
            edit_product_use_case(edit_request)

        assert str(captured_exception.value) == message_exception
        assert isinstance(captured_exception.value, type(expected_exception))