import pytest
from db.db import ProductsDB
from models.models import Product, User

@pytest.fixture(autouse=True)
def clean_products_and_users():
    db = ProductsDB()
    with db.session_scope() as session:
        session.query(User).delete()
        session.commit()

    yield
