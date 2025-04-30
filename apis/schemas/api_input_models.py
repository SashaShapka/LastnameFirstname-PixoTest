from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ProductClassification(str, Enum):
    education = "education"
    gaming = "gaming"
    home_goods = "home_goods"

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    in_stock: int
    classification: ProductClassification = Field(..., examples=["education"])

class ProductUpdateItem(BaseModel):
    id: str = Field(...)
    description: Optional[str] = Field(...,
                                       examples=["Python algorithms book"],
                                       description="describe main properties of product")
    price: Optional[float] = Field(...,
                                   gt=0,
                                   examples=[124,20])
    in_stock: Optional[int] = Field(...,
                                    ge=0,
                                    examples=[20],
                                    description="units of the product are available")

class ProductDeleteByIdInput(BaseModel):
    ids: List[str] = Field(...,examples=[["product_id_1", "product_id_1, ..."]])


class ChoseProductsInput(BaseModel):
    product_ids: List[str] = Field(..., examples=[["product_id_1", "product_id_1"]])


ProductUpdateInput = List[ProductUpdateItem]
ProductCreateInput = List[ProductCreate]



