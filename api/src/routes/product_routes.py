from typing import List

from fastapi import APIRouter, Depends

from app.src.use_cases import (
    ListProducts, 
    ListProductResponse, 
    FindProductById, 
    FindProductByIdResponse, 
    FindProductByIdRequest, 
    CreateProduct, 
    CreateProductResponse, 
    CreateProductRequest,
    EditProduct,
    EditProductRequest,
    EditProductResponse,
    DeleteProduct, 
    DeleteProductRequest,
    DeleteProductResponse,
    FilterProductsByStatus, 
    FilterProductsByStatusRequest,
    FilterProductsByStatusResponse
)
from ..dtos import (
    ProductBase,
    ListProductResponseDto, 
    CreateProductRequestDto,
    CreateProductResponseDto,
    FindProductByIdResponseDto,
    EditProductResponseDto,
    EditProductRequestDto,
    DeleteProductResponseDto,
    FilterProductsByStatusResponseDto,
    FilterProductsByStatusRequestDto
)
from factories.use_cases import (
    list_product_use_case, 
    find_product_by_id_use_case,
    create_product_use_case,
    edit_product_use_case,
    delete_product_use_case,
    filter_products_by_status
)
from app.src.core.models import Product

product_router = APIRouter(prefix="/products")

@product_router.get("/", response_model=ListProductResponseDto)
async def get_products(
    use_case: ListProducts = Depends(list_product_use_case)
) -> ListProductResponse:
    response = use_case()
    response_dto: ListProductResponseDto = ListProductResponseDto(
        products=[ProductBase(
            **{
                **product._asdict(),
                "status": product.status.value 
            }
        ) for product in response.products]
    )
    return response_dto

@product_router.get("/{product_id}", response_model=FindProductByIdResponseDto)
async def get_product_by_id(
    product_id: str,
    use_case: FindProductById = Depends(find_product_by_id_use_case)
) -> FindProductByIdResponse:
    response = use_case(FindProductByIdRequest(product_id=product_id))
    response_dto: FindProductByIdResponseDto = FindProductByIdResponseDto(**response._asdict())
    return response_dto

@product_router.post("/", response_model=CreateProductResponseDto)
async def create_product(
    request: CreateProductRequestDto,
    use_case: CreateProduct = Depends(create_product_use_case)
) -> CreateProductResponse:
    response = use_case(CreateProductRequest(
        product_id=request.product_id, 
        user_id=request.user_id, 
        name=request.name, 
        description=request.description, 
        price=request.price, 
        location=request.location, 
        status=request.status, 
        is_available=request.is_available
    ))
    response_dto: CreateProductResponseDto = CreateProductResponseDto(**response._asdict())
    return response_dto

@product_router.put("/", response_model=EditProductResponseDto)
async def edit_product(
    request: EditProductRequestDto,
    use_case: EditProduct = Depends(edit_product_use_case)
) -> EditProductResponse:
    response = use_case(EditProductRequest(
        product_id=request.product_id, 
        user_id=request.user_id, 
        name=request.name, 
        description=request.description, 
        price=request.price, 
        location=request.location, 
        status=request.status, 
        is_available=request.is_available
    ))
    response_dto: EditProductResponseDto = EditProductResponseDto(**response._asdict())
    return response_dto


@product_router.delete("/{product_id}", response_model=DeleteProductResponseDto)
async def delete_product(
    product_id: str,
    use_case: DeleteProduct = Depends(delete_product_use_case)
) -> DeleteProductResponse:
    response = use_case(DeleteProductRequest(
       product_id=product_id
    ))
    response_dto: DeleteProductResponseDto = DeleteProductResponseDto(**response._asdict())
    return response_dto

@product_router.get("/filter/status", response_model=FilterProductsByStatusResponseDto)
async def get_filtered_products_by_status(
    status: str,
    use_case: FilterProductsByStatus = Depends(filter_products_by_status)
) -> FilterProductsByStatusResponse:
    response = use_case(FilterProductsByStatusRequest(status))
    response_dto: FilterProductsByStatusResponseDto = FilterProductsByStatusResponseDto(
        products=[ProductBase(
            **{
                **product._asdict(),
                "status": product.status 
            }
        ) for product in response.products]
    )
    return response_dto
