from django import template

register = template.Library()


@register.filter
def local_static(path, app_directory):
    return app_directory + "/" + path
