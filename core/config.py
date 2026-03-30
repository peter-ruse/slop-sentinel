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

    @property
    def raw_password(self):
        return self.password.get_secret_value()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class RedisCacheSettings(BaseSettings):
    cache_ttl: int = Field(default=86400, validation_alias="CACHE_TTL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
