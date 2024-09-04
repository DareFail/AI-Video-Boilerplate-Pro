from ..utils import render_with_appname


def home(request):
    return render_with_appname(request, "index.html", {})


def room(request, room_name):
    return render_with_appname(request, "room.html", {"room_name": room_name})
