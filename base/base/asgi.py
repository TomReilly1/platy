"""
ASGI config for base project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""
import os
import django
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

django.setup()

django_asgi_app = get_asgi_application()


from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import platy.routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                platy.routing.websocket_urlpatterns
            )
        )
    )
    # 'websocket': AuthMiddlewareStack(
    #     URLRouter(
    #         platy.routing.websocket_urlpatterns
    #     )
    # )
})
 