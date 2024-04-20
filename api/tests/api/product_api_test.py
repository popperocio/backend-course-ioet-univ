from http import HTTPStatus
import pytest
from fastapi.testclient import TestClient

from api.src.create_app import create_app



def test__should_return_a_list_of_products(api_client):

    response = api_client.get("/products/")
    products = response.json().get("products")

    assert response.status_code == HTTPStatus.OK
    assert products == []
