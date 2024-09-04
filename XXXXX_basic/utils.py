from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string


def get_app_directory():
    app_directory = "XXXXX_basic"
    return app_directory


def add_appname(template_path):
    return get_app_directory() + "/" + template_path


def get_website_from_app():
    url_path = str(get_app_directory()) + ".urls"
    for x in range(len(settings.VIRTUAL_APPS)):
        if url_path == settings.VIRTUAL_APPS[x]:
            return settings.VIRTUAL_DOMAINS[x]

    return None


def render_with_appname(request, template_path, context={}, status=False):

    new_template_path = add_appname(template_path)

    if status:
        return render(
            request, new_template_path, context=context, status=status
        )
    else:
        return render(request, new_template_path, context=context)


def render_to_string_with_appname(template_path, context={}):

    new_template_path = add_appname(template_path)

    return render_to_string(new_template_path, context=context)
