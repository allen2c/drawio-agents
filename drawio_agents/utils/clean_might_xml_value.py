import typing

if typing.TYPE_CHECKING:
    import lxml.etree as ET


def clean_might_xml_value(
    value: str, *, parser: typing.Optional["ET.HTMLParser"] = None
) -> str:
    """
    Convert XML/HTML string to plaintext, converting <div> tags to newlines.
    Returns original string if parsing fails.

    Args:
        value: String that might be XML/HTML or plaintext

    Returns:
        Cleaned plaintext string
    """
    import lxml.etree as ET

    if not value or not value.strip():
        return ""

    parser = parser or ET.HTMLParser()

    try:
        from io import StringIO

        import lxml.etree as ET

        # Use HTML parser to handle fragments
        parser = ET.HTMLParser()
        tree = ET.parse(StringIO(value), parser)

        # Get the body or root element
        body = tree.xpath("//body")
        root = body[0] if body else tree.getroot()

        # Build text with proper div handling
        result_parts = []
        prev_was_div = False

        for element in root.iter():
            if element.tag == "div":
                # Add newline before div if there's already content
                if result_parts and not prev_was_div:
                    result_parts.append("\n")

                # Get all text content from this div
                div_text = "".join(element.itertext()).strip()
                if div_text:
                    result_parts.append(div_text)
                    result_parts.append("\n")

                prev_was_div = True
            elif element.tag not in ["html", "body"]:
                # For non-div elements, add their text if it's not already captured
                if element.text and element.getparent().tag != "div":
                    result_parts.append(element.text.strip())
                prev_was_div = False

        # Join and clean up
        result = "".join(result_parts).strip()
        # Remove extra newlines but preserve single newlines
        while "\n\n" in result:
            result = result.replace("\n\n", "\n")

        return result

    except ET.Error:
        # If parsing fails, return original string
        return value
