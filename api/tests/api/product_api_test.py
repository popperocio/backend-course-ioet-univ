from decimal import Decimal
from http import HTTPStatus
import pytest
import simplejson as json
from api.src.dtos import EditProductRequestDto, CreateProductRequestDto

def test__should_return_a_list_of_products(api_client):

    response = api_client.get("/products/")
    products = response.json().get("products")
    
    assert response.status_code == HTTPStatus.OK
    
def test__should_return_an_updated_product(api_client):
    request_create_data =  CreateProductRequestDto(
        product_id="17",
        user_id="1",
        name="Headphones",
        description="Noise cancellation",
        price=10.5,
        location="Quito",
        status="New",
        is_available=True,      
    )
    serialized_request_data_to_create = json.dumps(request_create_data.model_dump(), use_decimal=True)
    json_payload_to_create = json.loads(serialized_request_data_to_create)
    api_client.post("/products/", json=json_payload_to_create)
    request_edit_data = EditProductRequestDto(
        product_id="17",
        user_id="1",
        name="Headphones",
        description="Noise cancellation",
        price=3.9,
        location="Tandil",
        status="New",
        is_available=False,      
    )
    serialized_request_data = json.dumps(request_edit_data.model_dump(), use_decimal=True)
    json_payload = json.loads(serialized_request_data)
    response = api_client.put("/products/",json=json_payload)
   
    assert response.status_code == HTTPStatus.OK
    assert response.json()["product_id"] == request_create_data.product_id
    assert response.json()["location"] == "Tandil"
    assert response.json()["is_available"] == False
    

def test__should_return_a_deleted_product_id(api_client):
    request_create_data =  CreateProductRequestDto(
        product_id="99002",
        user_id="1",
        name="Headphones",
        description="Noise cancellation",
        price=10.5,
        location="Quito",
        status="New",
        is_available=True,      
    )
    serialized_request_data_to_create = json.dumps(request_create_data.model_dump(), use_decimal=True)
    json_payload_to_create = json.loads(serialized_request_data_to_create)
    api_client.post("/products/", json=json_payload_to_create)
    product_id = request_create_data.product_id

    response = api_client.delete(f"/products/{product_id}")
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()["product_id"] == product_id


def test__should_return_a_list_of_filtered_products_by_status(api_client, products_factory):
    products = products_factory(4)
    for product in products:
        request_create_data =  CreateProductRequestDto(
        product_id=product.product_id,
        user_id=product.user_id,
        name=product.name,
        description=product.description,
        price=product.price,
        location=product.location,
        status=product.status,
        is_available=product.is_available,      
        )
        serialized_request_data_to_create = json.dumps(request_create_data.model_dump(), use_decimal=True)
        json_payload_to_create = json.loads(serialized_request_data_to_create)
        api_client.post("/products/", json=json_payload_to_create)
    request = "For parts"
    response = api_client.get("/products/filter/status", params={"status": {request}})
   
    assert response.status_code == HTTPStatus.OK

    
