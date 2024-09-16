from common.customGroups.decorators import signedin

from ..utils import render_with_appname


@signedin
def signedin_home(request, group_unique):
    
    # uncomment if any model that needs to be made on signup with a foreign key to Group
    # profile = Profile.objects.filter(group=request.group).get_or_create(group=request.group)

    return render_with_appname(request, "signedin/index.html")
