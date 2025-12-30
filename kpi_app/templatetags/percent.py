from django import template

register = template.Library()

@register.filter
def percent(value, decimals=1):
    try:
        value = float(value) * 100
        format_str = f"{{:.{decimals}f}}%"
        return format_str.format(value)
    except (ValueError, TypeError):
        return ""

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
