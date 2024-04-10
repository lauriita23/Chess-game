"""
ASGI config for mychess project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mychess.settings')
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# get_asgi_application should go BEFORE import models !!
django_asgi_app = get_asgi_application()
import models.routing
application = ProtocolTypeRouter(
    {
        'http': django_asgi_app,
        'websocket': AuthMiddlewareStack(
            AuthMiddlewareStack(
                URLRouter(
                    models.routing.websocket_urlpatterns
                    )
            ),
        )
    }
)