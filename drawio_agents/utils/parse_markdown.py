import typing

import frontmatter
import yaml


def parse_markdown(markdown_text: str) -> tuple[typing.Dict[str, typing.Any], str]:
    """
    Parse Markdown string and separate YAML Front Matter from content.

    Args:
        markdown_text: Markdown string with or without YAML Front Matter.

    Returns:
        Tuple of (metadata dict, content string).
    """
    try:
        post = frontmatter.loads(markdown_text)
        return post.metadata, post.content

    except yaml.YAMLError as e:
        print(f"YAML format error: {e}")
        return {}, markdown_text
