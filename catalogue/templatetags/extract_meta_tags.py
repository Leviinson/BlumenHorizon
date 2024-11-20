from django import template
import re

register = template.Library()

@register.filter
def extract_meta_tags(value, tag):
    """Фильтр для извлечения значения мета-тега из HTML-кода"""
    if tag == "title":
        match = re.search(r'<title>(.*?)</title>', value)
        return match.group(1) if match else ""
    elif tag == "description":
        match = re.search(r'<meta name="description" content="(.*?)">', value)
        return match.group(1) if match else ""
    return ""