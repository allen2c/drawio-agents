import logging
import secrets
import typing

import pydantic

if typing.TYPE_CHECKING:
    import lxml.etree as ET

logger = logging.getLogger(__name__)


class Edge(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=lambda: secrets.token_urlsafe(16))
    source: str
    target: str
    parent: str | None = None
    edge: typing.Literal["1"] = "1"

    @classmethod
    def from_xml(
        cls, xml_content: bytes, *, parser: typing.Optional["ET.XMLParser"] = None
    ):
        """Parse draw.io XML content and extract edges."""
        import lxml.etree as ET
        from str_or_none import str_or_none

        parser = parser or ET.XMLParser()
        root = ET.fromstring(xml_content, parser)

        edges = []
        for idx, cell in enumerate(root.xpath("//mxCell[@edge='1']")):
            _edge_data = {}

            if _id := str_or_none(cell.get("id", None)):
                _edge_data["id"] = _id

            if _source := str_or_none(cell.get("source", None)):
                _edge_data["source"] = _source

            if _target := str_or_none(cell.get("target", None)):
                _edge_data["target"] = _target

            if _parent := str_or_none(cell.get("parent", None)):
                _edge_data["parent"] = _parent

            if _edge := str_or_none(cell.get("edge", None)):
                _edge_data["edge"] = _edge

            try:
                edges.append(cls.model_validate(_edge_data))
            except pydantic.ValidationError as e:
                logger.error(f"Error validating edge {idx}: {cell}")
                raise e

        return edges
