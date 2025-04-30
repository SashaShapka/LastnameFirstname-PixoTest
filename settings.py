from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    redis_host: str = "localhost"
    redis_port: int = 6379
    success_timeout: int = 3600
    failed_timeout: int = 60
    redis_db: int = 0
    use_cache: bool = True
    postgres_db_name: str = "products"
    postgres_db_test_name: str = "products_test"
    postgres_db_user: str = "admin"
    postgres_db_test_user: str = "test_admin"
    postgres_db_host: str = "127.0.0.1"
    postgres_db_port: str = "5432"
    postgres_db_password: str = "products"
    jwt_algorithm: str = "HS256"
    jwt_secret: str = "secret"
    jwt_expires_s: int = 3600
    enable_rate_limit: bool = True
    rate_limit_default: str = "20/minute"


    class Config:
        env_file = ".env"

settings = Settings()