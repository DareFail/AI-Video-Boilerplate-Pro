from ..utils import render_with_appname


def home(request):
    context = {}
    return render_with_appname(request, "index.html", context=context)
