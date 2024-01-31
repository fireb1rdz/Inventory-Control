from django import template


register = template.Library()

@register.filter(name="quantity_filter")
def format_quantity(value):
    if value == int(value):
        return f"{int(value)}"
    return f"{value:.2f}"