from typing import Annotated

from pydantic import AfterValidator, Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


def strip_slash(url: HttpUrl) -> str:
    return url.encoded_string().rstrip("/")


CleanUrl = Annotated[HttpUrl, AfterValidator(strip_slash)]


class GitHubSettings(BaseSettings):
    api_base_url: CleanUrl = Field(
        default=HttpUrl("https://api.github.com"),
        validation_alias="GITHUB_API_BASE_URL",
    )
    token: SecretStr = Field(validation_alias="GITHUB_TOKEN")
    per_page: int = Field(default=100, validation_alias="GITHUB_PER_PAGE")
    max_parallel: int = Field(default=10, validation_alias="GITHUB_MAX_PARALLEL")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def raw_token(self):
        return self.token.get_secret_value()


class RedisSettings(BaseSettings):
    host: str = Field(default="localhost", validation_alias="REDIS_HOST")
    port: int = Field(default=6379, validation_alias="REDIS_PORT")
    db: int = Field(default=0, validation_alias="REDIS_DB")
    password: SecretStr = Field(validation_alias="REDIS_PASSWORD")
    socket_timeout: float = Field(default=5.0, validation_alias="REDIS_SOCKET_TIMEOUT")
    socket_connect_timeout: float = Field(
        default=5.0, validation_alias="REDIS_SOCKET_CONNECT_TIMEOUT"
    )

    @property
    def raw_password(self):
        return self.password.get_secret_value()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class PostgreSQLSettings(BaseSettings):
    user: str = Field(validation_alias="POSTGRES_USER")
    password: str = Field(validation_alias="POSTGRES_PASSWORD")
    host: str = Field(default="db", validation_alias="POSTGRES_HOST")
    port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    db: str = Field(validation_alias="POSTGRES_DB")

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class JWTSettings(BaseSettings):
    secret_key: SecretStr = Field(validation_alias="SECRET_KEY")

    @property
    def raw_secret_key(self):
        return self.secret_key.get_secret_value()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


github_settings = GitHubSettings()  # type: ignore
redis_settings = RedisSettings()  # type: ignore
postgresql_settings = PostgreSQLSettings()  # type: ignore
jwt_settings = JWTSettings()  # type: ignore
