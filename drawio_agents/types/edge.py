import pydantic
import secrets
import typing


class Edge(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=lambda: secrets.token_urlsafe(16))
    source: str
    target: str
    parent: str | None = None
    edge: typing.Literal["1"] = "1"
