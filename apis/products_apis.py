from typing import Optional

from fastapi import Request
from fastapi import Depends
from fastapi import Query


from apis.schemas.api_input_models import ProductCreateInput, ProductUpdateInput, ProductDeleteByIdInput, \
    ChoseProductsInput
from apis.schemas.user_input_model import User


from cache.redis_utils import cache_response
from limiter import conditional_limiter

from services.auth import get_admin_user, get_current_user
from services.products import ProductsService
from settings import settings


@conditional_limiter(settings.rate_limit_default)
@cache_response()
async def get_products(
    request: Request,
    _: User = Depends(get_current_user),
    products_service: ProductsService = Depends()
):
    data = await products_service.get_products()
    return data

@conditional_limiter(settings.rate_limit_default)
@cache_response()
async def get_product_by_filters(
    request: Request,
    name: Optional[str] = Query(None, description="Filter by name"),
    price_min: Optional[float] = Query(None, description="Minimum price"),
    price_max: Optional[float] = Query(None, description="Maximum price"),
    price_exact: Optional[float] = Query(None, description="Exact price"),
    classification: Optional[str] = Query(None, description="Product classification"),
    _: User = Depends(get_current_user),
    products_service: ProductsService = Depends()
):

    data = await products_service.get_products_by_filters(filters = {
                                                                "name": name,
                                                                "price_min": price_min,
                                                                "price_max": price_max,
                                                                "price_exact": price_exact,
                                                                "classification": classification
                                                                }
                                                    )


    return data

@conditional_limiter(settings.rate_limit_default)
async def create_products(
    request: Request,
    products_data: ProductCreateInput,
    _: User = Depends(get_admin_user),
    products_service: ProductsService = Depends()
):
    data =  await products_service.create(products_data)
    return data

@conditional_limiter(settings.rate_limit_default)
async def update_products(
        request: Request,
        updates: ProductUpdateInput,
        _: User = Depends(get_admin_user),
        products_service: ProductsService = Depends()
):
    data =  await products_service.update(updates)
    return data

@conditional_limiter(settings.rate_limit_default)
async def delete_products(
        request: Request,
        delete_input: ProductDeleteByIdInput,
        _: User = Depends(get_admin_user),
        products_service: ProductsService = Depends()
):
    data = await products_service.delete(delete_input)
    return data

@conditional_limiter(settings.rate_limit_default)
async def chose_products(
        request: Request,
        chose_input: ChoseProductsInput,
        current_user : User = Depends(get_current_user),
        products_service: ProductsService = Depends()
):
    data = await products_service.chose_products(chose_input, current_user.id)
    return data



@conditional_limiter(settings.rate_limit_default)
@cache_response()
async def get_statistic(
    request: Request,
    values_on_the_top: int = Query(3, ge=1, description="Values on the top"),
    _: User = Depends(get_admin_user),
    products_service: ProductsService = Depends()

):
    data = await products_service.get_statistic_by_most_common(values_on_the_top)
    return data