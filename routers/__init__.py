from fastapi import APIRouter
from routers.definitions import *
from routers.auth_definitions import *
import logging


logger = logging.getLogger('my_logger')


router = APIRouter()

def register_routes(app):

    logger.info("Subscribe apis methods")

    router.add_api_route(
        path=GetProductsDefinition.URI,
        endpoint=GetProductsDefinition.API,
        methods=GetProductsDefinition.METHODS,
        response_model=GetProductsDefinition.RESPONSE_MODEL
    )

    router.add_api_route(
        path=GetProductsByFilter.URI,
        endpoint=GetProductsByFilter.API,
        methods=GetProductsByFilter.METHODS,
        response_model=GetProductsByFilter.RESPONSE_MODEL
    )

    router.add_api_route(
        path=CreateProductsDefinition.URI,
        endpoint=CreateProductsDefinition.API,
        methods=CreateProductsDefinition.METHODS,
        response_model=CreateProductsDefinition.RESPONSE_MODEL
    )

    router.add_api_route(
        path=UpdateProductsDefinition.URI,
        endpoint=UpdateProductsDefinition.API,
        methods=UpdateProductsDefinition.METHODS,
        response_model=UpdateProductsDefinition.RESPONSE_MODEL
    )

    router.add_api_route(
        path=DeleteProductsDefinition.URI,
        endpoint=DeleteProductsDefinition.API,
        methods=DeleteProductsDefinition.METHODS,
        response_model=DeleteProductsDefinition.RESPONSE_MODEL
    )

    router.add_api_route(
        path=GetStatisticDefinition.URI,
        endpoint=GetStatisticDefinition.API,
        methods=GetStatisticDefinition.METHODS,
        response_model=GetStatisticDefinition.RESPONSE_MODEL
    )


    router.add_api_route(
        path=GetStatisticDefinition.URI,
        endpoint=GetStatisticDefinition.API,
        methods=GetStatisticDefinition.METHODS,
        response_model=GetStatisticDefinition.RESPONSE_MODEL
    )

    router.add_api_route(
        path=SingUpDefinition.URI,
        endpoint=SingUpDefinition.API,
        methods=SingUpDefinition.METHODS,
        response_model=SingUpDefinition.RESPONSE_MODEL
    )

    router.add_api_route(
        path=SingInDefinition.URI,
        endpoint=SingInDefinition.API,
        methods=SingInDefinition.METHODS,
        response_model=SingInDefinition.RESPONSE_MODEL
    )

    router.add_api_route(
        path=GetUserDefinition.URI,
        endpoint=GetUserDefinition.API,
        methods=GetUserDefinition.METHODS,
        response_model=GetUserDefinition.RESPONSE_MODEL
    )

    router.add_api_route(
        path=ChoseProductsDefinition.URI,
        endpoint=ChoseProductsDefinition.API,
        methods=ChoseProductsDefinition.METHODS,
        response_model=ChoseProductsDefinition.RESPONSE_MODEL
    )

    app.include_router(router)