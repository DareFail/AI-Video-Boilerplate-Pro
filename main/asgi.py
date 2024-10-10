import os
import importlib
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.middleware import BaseMiddleware
from channels.routing import get_default_application
from django.core.asgi import get_asgi_application
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

ASGI_APPLICATION = {}

for domain, app in zip(settings.VIRTUAL_DOMAINS, settings.VIRTUAL_APPS):
    app_name = app.split('.')[0]  # Assuming app is defined as "app_name.urls"
    try:
        routing_module = importlib.import_module(f"{app_name}.routing")
        ASGI_APPLICATION[domain] = URLRouter(routing_module.websocket_urlpatterns)
    except (ImportError, AttributeError):
        print(f"No websockets for {domain}/{app}")
    
class DynamicRouter(BaseMiddleware):
    def __init__(self, inner, application_mapping=None):
        super(DynamicRouter, self).__init__(inner)
        self.application_mapping = application_mapping or {}

    async def __call__(self, scope, receive, send):
        # Extract host
        host = dict(scope['headers']).get(b'host')
        if host:
            host = host.decode()

        # Try to find application
        application = self.application_mapping.get(host, get_default_application())

        # Call application
        return await application(scope, receive, send)

application = ProtocolTypeRouter(
    {
        # Django's ASGI application for HTTP
        "http": get_asgi_application(),
        # Django Channels' route for websocket
        "websocket": AuthMiddlewareStack(
            DynamicRouter(URLRouter([]), ASGI_APPLICATION),
        ),
    }
)
