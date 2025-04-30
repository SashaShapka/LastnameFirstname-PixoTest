from urllib.parse import quote_plus as urlquote
from settings import settings
import logging


logger = logging.getLogger('my_logger')

class Singleton(type):
    """
    Singleton meta class.
    :see: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_connection_string(db_name):
    host = "127.0.0.1"
    port = "5432"
    user = (
        settings.postgres_db_test_user
        if db_name == settings.postgres_db_test_name
        else settings.postgres_db_user
    )
    password = settings.postgres_db_password
    return f"postgresql://{urlquote(user)}:{urlquote(password)}@{urlquote(host)}:{urlquote(port)}/{urlquote(db_name)}"



def init_db():
    logger.info("Extend db with models")
    from db.db import ProductsDB

    _ = ProductsDB()