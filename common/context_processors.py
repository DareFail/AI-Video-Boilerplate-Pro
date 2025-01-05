from django.conf import settings
from common.utils import appname_from_request


def global_context(request):
    global_context = {
        "APP_DIRECTORY": appname_from_request(request),
        "HOST": request.get_host(),
        "HTTP": get_http(),
        "PATH": request.path,
        "SMARKETMAN_LINK": settings.SMARKETMAN_LINK,
    }

    if not settings.DEBUG:
        global_context["GOOGLE_ANALYTICS_ID"] = getAnalytics(
            request.get_host()
        )
        return global_context
    else:
        return global_context
    
def get_http():
    if settings.LOCAL_DEV:
        return "http://"
    return "https://"


def getAnalytics(host):
    virtual_hosts = {}

    for x in range(len(settings.VIRTUAL_DOMAINS)):
        virtual_hosts[settings.VIRTUAL_DOMAINS[x]] = (
            settings.VIRTUAL_GOOGLE_ANALYTICS[x]
        )

    return virtual_hosts.get(host, False)
