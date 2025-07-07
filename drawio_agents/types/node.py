import pydantic
import secrets
import typing


class Node(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=lambda: secrets.token_urlsafe(16))
    value: str = ""
    vertex: typing.Literal["1"] = "1"
