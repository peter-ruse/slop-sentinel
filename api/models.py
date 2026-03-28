from typing import Annotated

from pydantic import AfterValidator, BaseModel, HttpUrl


def http_url_to_str(url: HttpUrl) -> str:
    return url.encoded_string()


class RepoRequest(BaseModel):
    url: Annotated[HttpUrl, AfterValidator(http_url_to_str)]
