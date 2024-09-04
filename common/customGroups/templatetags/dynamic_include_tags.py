from django import template

register = template.Library()


@register.simple_tag
def include_dynamic(value, arg):
    """usage: {% include_dynamic APP_DIRECTORY 'subfolder/file.html' %}"""
    return "".join([value, "/", arg])
