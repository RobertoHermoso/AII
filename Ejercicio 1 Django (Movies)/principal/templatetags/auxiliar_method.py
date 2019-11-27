from django import template

register = template.Library()


@register.inclusion_tag('directores.html')
@register.inclusion_tag('peliculas.html')
@register.filter("filter")
def get_list_peliculas(mapa, key):
    res = []
    res = mapa[key]
    print(mapa[key])
    return res