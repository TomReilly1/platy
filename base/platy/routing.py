from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/(?P<sender>[\w-]+)/(?P<target>[\w-]+)/$', consumers.ChatConsumer.as_asgi())
]
