from django import template

register = template.Library()

@register.filter
def chunked(items, chunk_size):
    """Разбивает список на чанки заданного размера."""
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]
