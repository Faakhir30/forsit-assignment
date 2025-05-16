from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "E-commerce Admin API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "123"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_DATABASE: str = "ecommerce_admin"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"mysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
