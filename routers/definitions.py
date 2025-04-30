from apis.products_apis import get_products, create_products, update_products, delete_products, get_statistic, \
    chose_products, get_product_by_filters

from apis.schemas.api_response_models import *

class GetProductsDefinition:
    URI = '/get_products'
    API = get_products
    METHODS = ["GET"]
    RESPONSE_MODEL = ProductResponse


class CreateProductsDefinition:
    URI = '/create_products'
    API = create_products
    METHODS = ["POST"]
    RESPONSE_MODEL = ProductCreateResponse


class UpdateProductsDefinition:
    URI = '/update_products'
    API = update_products
    METHODS = ["PUT"]
    RESPONSE_MODEL = ProductUpdateResponse


class DeleteProductsDefinition:
    URI = '/delete_products'
    API = delete_products
    METHODS = ["DELETE"]
    RESPONSE_MODEL = ProductDeleteResponse


class ChoseProductsDefinition:
    URI = '/chose_products'
    API = chose_products
    METHODS = ["POST"]
    RESPONSE_MODEL = ProductChoseResponse


class GetStatisticDefinition:
    URI = '/statistic_product'
    API = get_statistic
    METHODS = ["GET"]
    RESPONSE_MODEL = MostChosenProductResponse


class GetProductsByFilter:
    URI = '/get_products_by_filter'
    API = get_product_by_filters
    METHODS = ["GET"]
    RESPONSE_MODEL = ProductResponse