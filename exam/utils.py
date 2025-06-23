import re

import bleach
import markdown


def sanitize_and_render_markdown(text: str) -> str:
    allowed_tags = [
        "p",
        "br",
        "strong",
        "b",
        "em",
        "i",
        "u",
        "s",
        "del",
        "h1",
        "h2",
        "h3",
        "ul",
        "ol",
        "li",
        "blockquote",
        "code",
        "pre",
        "a",
        "img",
    ]

    allowed_attributes = {
        "a": ["href", "title"],
        "img": ["src", "alt", "title"],
    }

    md = markdown.Markdown(
        extensions=["fenced_code", "codehilite", "nl2br", "tables"],
        extension_configs={"codehilite": {"css_class": "highlight"}},
    )

    html = md.convert(text)
    return bleach.clean(
        html, tags=allowed_tags, attributes=allowed_attributes, strip=True
    )


def strip_markdown_to_text(text: str) -> str:
    text = re.sub(r"^#{1,3}\s+", "", text, flags=re.MULTILINE)

    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)

    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)

    text = re.sub(r"`([^`]+)`", r"\1", text)

    text = re.sub(r"^[\s]*[-\*\+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[\s]*\d+\.\s+", "", text, flags=re.MULTILINE)

    return text.strip()
