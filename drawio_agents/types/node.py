import logging
import secrets
import typing

import pydantic

if typing.TYPE_CHECKING:
    import lxml.etree as ET

logger = logging.getLogger(__name__)


class Node(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=lambda: secrets.token_urlsafe(16))
    value: str = ""
    vertex: typing.Literal["1"] = "1"

    @classmethod
    def from_xml(
        cls, xml_content: bytes, *, parser: typing.Optional["ET.XMLParser"] = None
    ):
        import lxml.etree as ET
        from str_or_none import str_or_none

        parser = parser or ET.XMLParser()
        root = ET.fromstring(xml_content, parser)

        vertex_cells: typing.List[ET._Element] = root.xpath("//mxCell[@vertex='1']")

        nodes = []
        for idx, cell in enumerate(vertex_cells):
            _node_data = {}
            if _id := str_or_none(cell.get("id", None)):
                _node_data["id"] = _id
            if _value := str_or_none(cell.get("value", None)):
                _clean_value = (
                    _value.replace("&lt;", "<")
                    .replace("&gt;", ">")
                    .replace("&quot;", '"')
                    .replace("&amp;", "&")
                    .replace("&apos;", "'")
                    .replace("&nbsp;", " ")
                )
                _node_data["value"] = _clean_value
            if _vertex := str_or_none(cell.get("vertex", None)):
                _node_data["vertex"] = _vertex

            try:
                nodes.append(cls.model_validate(_node_data))
            except pydantic.ValidationError as e:
                logger.error(f"Error validating node {idx}: {cell}")
                raise e

        return nodes
