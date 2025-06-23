from django import template

register = template.Library()

@register.filter
def percent(value, decimals=0):
    try:
        return f"{round(float(value) * 100, int(decimals))}%"
    except (ValueError, TypeError):
        return ""
