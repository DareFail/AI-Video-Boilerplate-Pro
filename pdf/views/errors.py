from ..utils import render_with_appname

def handle_404(request):
    context = {}
    return render_with_appname(request, "404.html", context=context, status=404)

def handle_500(request):
    context = {}
    return render_with_appname(request, "500.html", context=context, status=500)