import contextlib

import sqlalchemy.orm
from db.db_utils import Singleton, get_connection_string
from models import models
from settings import settings
import logging

logger = logging.getLogger('my_logger')

class ProductsDB(metaclass=Singleton):

    def __init__(self, timeout=60, create_all=False):

        self.is_closed = False
        self.engine = sqlalchemy.create_engine(get_connection_string(settings.postgres_db_name))
        self.engine.pool_timeout = timeout
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)

        if create_all:
            try:
                models.Base.metadata.create_all(self.engine)
            except Exception as e:
                logger.error(f"Error during create_all method {e}")
                raise

    def __del__(self):
        """
        Calls the close method
        """
        try:
            self.close()
        except Exception:
            pass

    def close(self):
        """
        Closes the connections and disposes the engine
        """
        if self.is_closed or self.engine is None:
            return

        self.engine.dispose()
        self.is_closed = True

    @contextlib.contextmanager
    def session_scope(self, to_commit=True):
        """
        Context manager for creating and using the SQL session
        :param to_commit: True if the session needs to be committed at the end
        :return: Session object
        """
        session = self.session(expire_on_commit=False)
        try:
            yield session
        except Exception as err:
            session.rollback()
            raise
        finally:
            session.close()