from pydantic_settings import BaseSettings


class ServerSettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000


class DatabaseSettings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/test"
    direct_url: str = "postgresql://postgres:postgres@localhost:5432/test"


server_settings = ServerSettings()
database_settings = DatabaseSettings()
