from django import template

register = template.Library()


@register.simple_tag
def philosophy_year(year):
    if year is None:
        return "Рік невідомий"

    if year < 0:
        return f"{abs(year)} р. до н. е."

    return f"{year} р. н. е."
