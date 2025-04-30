import logging
from functools import wraps

from sqlalchemy import delete
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from fastapi import HTTPException

from apis.schemas.api_input_models import ProductCreate
from apis.schemas.api_response_models import ProductCreateModel, ProductUpdateModel, ProductDeleteResponse, \
    ProductCreateResponse, ProductDeleteModel, ProductUpdateResponse, ChosenProductModel, ProductModel, \
    MostChosenProductModel, ProductResponse, MostChosenProductResponse, ProductChoseResponse

from db.db import ProductsDB
from models.models import *

logger = logging.getLogger("my_logger")

db = ProductsDB()


def db_safe(default_exception_msg="Unexpected DB error"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException:
                raise
            except SQLAlchemyError as e:
                logger.error(f"[DB] SQLAlchemyError in {func.__name__}: {e}")
                raise HTTPException(status_code=500, detail="Database error")
            except Exception as e:
                logger.error(f"[APP] Unexpected error in {func.__name__}: {e}")
                raise HTTPException(status_code=500, detail=default_exception_msg)
        return wrapper
    return decorator




class ProductsService:

    @db_safe("Error during product creation")
    async def create(self, products_data) -> ProductCreateResponse:
            logger.info("[Product] Product/products creation")
            if isinstance(products_data, ProductCreate):
                products_data = [products_data]
            with db.session_scope() as session:
                new_products = [
                    Product(
                        name=item.name,
                        description=item.description,
                        price=item.price,
                        in_stock=item.in_stock,
                        classification=item.classification.value,
                    )
                    for item in products_data
                ]

                session.add_all(new_products)
                session.flush()

                created_models = [
                    ProductCreateModel.model_validate(p) for p in new_products
                ]

                session.commit()

            return created_models

    @db_safe("Error during product creation")
    async def update(self, updates) -> ProductUpdateResponse:
            with db.session_scope() as session:
                product_map = {
                    product.id: product
                    for product in session.query(Product).filter(Product.id.in_([item.id for item in updates]))
                }

                updated_ids = []

                for item in updates:
                    product = product_map.get(item.id)
                    if not product:
                        raise HTTPException(status_code=404, detail=f"Product {item.id} not found")

                    if item.description is not None:
                        product.description = item.description
                    if item.price is not None:
                        product.price = item.price
                    if item.in_stock is not None:
                        product.in_stock = item.in_stock

                    updated_ids.append(ProductUpdateModel.model_validate(product))

                session.commit()

            return updated_ids

    @db_safe("Error during product creation")
    async def delete(self, delete_input)-> ProductDeleteResponse :

        with db.session_scope() as session:
            existing_ids = session.query(Product.id).filter(Product.id.in_(delete_input.ids)).all()
            existing_ids = [id_tuple[0] for id_tuple in existing_ids]

            if not existing_ids:
                raise HTTPException(status_code=404, detail="No matching products found")

            session.execute(delete(Product).where(Product.id.in_(existing_ids)))
            session.commit()

            return ProductDeleteModel(deleted_ids=existing_ids)

    @db_safe("Error during product creation")
    async def chose_products(self, chose_inputs, current_user_id) -> ProductChoseResponse:
        product_ids = chose_inputs.product_ids

        with db.session_scope() as session:
            products = session.query(Product).filter(Product.id.in_(product_ids)).all()
            existing_ids = {p.id for p in products}
            missing_ids = set(product_ids) - existing_ids
            if missing_ids:
                raise HTTPException(status_code=404, detail=f"Products not found: {missing_ids}")

            existing_links = session.query(UserProductRequest).filter(
                UserProductRequest.user_id == str(current_user_id),
                UserProductRequest.product_id.in_(existing_ids)
            ).all()
            existing_ids_with_links = {link.product_id for link in existing_links}

            now = datetime.now(timezone.utc)
            new_links = [
                UserProductRequest(
                    user_id=str(current_user_id),
                    product_id=pid,
                    requested_at=now
                )
                for pid in existing_ids - existing_ids_with_links
            ]
            session.bulk_save_objects(new_links)

            requested_map = {link.product_id: link.requested_at for link in existing_links}
            for link in new_links:
                requested_map[link.product_id] = link.requested_at

            result_products = []
            for product in products:
                product.requested_at = requested_map.get(product.id)
                result_products.append(ChosenProductModel.model_validate(product))

            session.commit()
            return result_products

    @db_safe("Error during product creation")
    async def get_products(self) -> ProductResponse:
            with db.session_scope() as session:
                products = session.query(Product).all()
                products = [ProductModel.model_validate(p, from_attributes=True) for p in products]

                return products

    @db_safe("Error during product creation")
    async def get_products_by_filters(self, filters: dict) -> ProductResponse or []:

        if filters.get("classification"):
            try:
               ProductClassification(filters.get("classification"))
            except ValueError:
                return []
        with db.session_scope() as session:
            query = session.query(Product)

            if filters:
                if filters.get("name"):
                    query = query.filter(Product.name.ilike(f"%{filters['name']}%"))
                if filters.get("price_exact") is not None:
                    query = query.filter(Product.price == filters["price_exact"])
                else:
                    if filters.get("price_min") is not None:
                        query = query.filter(Product.price >= filters["price_min"])
                    if filters.get("price_max") is not None:
                        query = query.filter(Product.price <= filters["price_max"])
                if filters.get("classification"):
                    query = query.filter(Product.classification == filters["classification"])

            products = query.all()
            return [ProductModel.model_validate(p, from_attributes=True) for p in products]

    @db_safe("Error during product creation")
    async def get_statistic_by_most_common(self, values_on_the_top: int) -> MostChosenProductResponse:
        with db.session_scope() as session:

            data = (
                session.query(
                    Product.id.label("product_id"),
                    Product.name.label("name"),
                    func.count(UserProductRequest.id).label("times_chosen")
                )
                .join(UserProductRequest, Product.id == UserProductRequest.product_id)
                .group_by(Product.id)
                .order_by(func.count(UserProductRequest.id).desc())
                .limit(values_on_the_top)
                .all()
            )

            data_result = [
                MostChosenProductModel.model_validate(row._asdict())
                for row in data
            ]

            return data_result