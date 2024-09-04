from django.conf import settings


def appname_from_request(request):
    virtual_hosts = {}

    for x in range(len(settings.VIRTUAL_DOMAINS)):
        virtual_hosts[settings.VIRTUAL_DOMAINS[x]] = settings.VIRTUAL_APPS[x]

    return virtual_hosts.get(request.get_host(), "").split(".")[0]
