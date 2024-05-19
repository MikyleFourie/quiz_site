"""
ASGI config for quiz_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.urls import re_path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import userProfiles.routing

# from quiz import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_site.settings')

application = ProtocolTypeRouter({
    "https": get_asgi_application(),
    "websocket": 
    AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(userProfiles.routing.websocket_urlpatterns)
        ),
    )
})



#application = get_asgi_application()
