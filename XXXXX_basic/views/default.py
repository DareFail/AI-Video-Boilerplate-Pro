from ..utils import render_with_appname


def home(request):
    return render_with_appname(request, "index.html")
