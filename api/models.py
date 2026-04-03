from typing import Annotated

from pydantic import AfterValidator, BaseModel, HttpUrl, SecretStr


def http_url_to_str(url: HttpUrl) -> str:
    return url.encoded_string()


class RepoRequest(BaseModel):
    url: Annotated[HttpUrl, AfterValidator(http_url_to_str)]


class UserRegistration(BaseModel):
    username: str
    password: SecretStr

    @property
    def raw_password(self):
        return self.password.get_secret_value()
