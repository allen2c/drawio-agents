"""Node representation for draw.io diagrams.

Contains the Node class for modeling vertices/nodes in draw.io XML files.
"""

import logging
import secrets
import typing

import pydantic

if typing.TYPE_CHECKING:
    import lxml.etree as ET

logger = logging.getLogger(__name__)


class Node(pydantic.BaseModel):
    """Represents a vertex/node in a draw.io diagram.

    Contains an identifier, text value, and vertex marker.
    """

    id: str = pydantic.Field(default_factory=lambda: secrets.token_urlsafe(16))
    value: str = ""
    vertex: typing.Literal["1"] = "1"

    @classmethod
    def from_xml(
        cls, xml_content: bytes, *, parser: typing.Optional["ET.XMLParser"] = None
    ):
        """Parse draw.io XML content and extract vertex nodes.

        Returns a list of Node instances from mxCell elements with vertex='1'.
        """
        import lxml.etree as ET
        from str_or_none import str_or_none

        from drawio_agents.utils.clean_might_xml_value import clean_might_xml_value

        parser = parser or ET.XMLParser()
        root = ET.fromstring(xml_content, parser)

        vertex_cells: typing.List[ET._Element] = root.xpath("//mxCell[@vertex='1']")

        nodes = []
        for idx, cell in enumerate(vertex_cells):
            _node_data = {}

            if _id := str_or_none(cell.get("id", None)):
                _node_data["id"] = _id

            if _value := str_or_none(cell.get("value", None)):
                _clean_value = clean_might_xml_value(_value, parser=parser)
                _node_data["value"] = _clean_value

            if _vertex := str_or_none(cell.get("vertex", None)):
                _node_data["vertex"] = _vertex

            try:
                nodes.append(cls.model_validate(_node_data))
            except pydantic.ValidationError as e:
                logger.error(f"Error validating node {idx}: {cell}")
                raise e

        return nodes
