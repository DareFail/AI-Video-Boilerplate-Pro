from common.customGroups.decorators import signedin

from ..utils import render_with_appname


@signedin
def signedin_home(request, group_unique):
    return render_with_appname(request, "signedin/index.html")
