import enum
from functools import lru_cache, cached_property
from typing import Any
import hmac
import hashlib
from pydantic_settings import BaseSettings
from sqlalchemy.engine.url import URL
import ssl

class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    # Application settings
    debug: bool = False
    title: str = "WYD API"
    version: str = "0.1.0"

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    postgres_host: str | None = None
    postgres_port: int | None = None
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_connection_name: str | None = None
    postgres_echo: bool = False


    # tg bot variables
    tg_token: str
    tg_wh_secret: str

    url_address: str = "https://test.wyd.ing"

    stat_tg_token: str



    @property
    def tg_webhook_url(self) -> str:
        return f"{self.url_address}/api/webhook"
    

    @cached_property
    def tg_secret_key_bytes(self) -> bytes:
        return hmac.new("WebAppData".encode(), self.tg_token.encode(), hashlib.sha256).digest()



    @property
    def fastapi_config(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
        }

    @property
    def db_url(self) -> URL:
        if self.postgres_connection_name:
            return URL.create(
                drivername="postgresql+asyncpg",
                username=self.postgres_user,
                password=self.postgres_password,
                database=self.postgres_db,
                query={"host": f"/cloudsql/{self.postgres_connection_name}"},
            )
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )
    
    @property
    def db_connections_args(self) -> dict[str, Any]:

        ssl_ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        if self.postgres_host != 'localhost':
            connect_args = {"ssl": ssl_ctx}
        else:
            connect_args = {}
        return connect_args

@lru_cache
def get_settings() -> Settings:
    return Settings()
