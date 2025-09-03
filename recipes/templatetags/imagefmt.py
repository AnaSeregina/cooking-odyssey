import os
from django import template

register = template.Library()

@register.filter
def remove_ext(url: str) -> str:
    """Return URL without its file extension (everything after the last dot)."""
    if not url:
        return url
    root, _ext = os.path.splitext(url)
    return root
