from django import template


register = template.Library()

@register.filter(name="format_quantity")
def format_quantity(value):
    if value == int(value):
        return f"{int(value)}"
    return f"{value:.2f}"