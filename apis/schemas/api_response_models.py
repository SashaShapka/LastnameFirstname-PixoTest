from pydantic import BaseModel
from apis.schemas.api_input_models import ProductCreate
from typing import List, Union
from datetime import datetime
from uuid import UUID


class ProductModel(BaseModel):
    id: str
    name: str
    description: str
    price: float
    in_stock: int
    classification: str
    created_at: datetime
    updated_at: datetime



class ProductCreateModel(ProductCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class ProductUpdateModel(ProductModel):
    model_config = {
        "from_attributes": True
    }



class ProductDeleteModel(BaseModel):
    deleted_ids: List[str]
    message: str = "Products successfully deleted"


class ChosenProductModel(ProductCreateModel):
    requested_at: datetime


class MostChosenProductModel(BaseModel):
    product_id: str
    name: str
    times_chosen: int


ProductResponse = List[ProductModel]
ProductCreateResponse = List[ProductCreateModel]
ProductUpdateResponse = List[ProductUpdateModel]
ProductDeleteResponse = Union[ProductDeleteModel]
ProductChoseResponse = List[ChosenProductModel]
MostChosenProductResponse = List[MostChosenProductModel]