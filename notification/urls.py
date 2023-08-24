from . import consumers
from django.urls import re_path, path

from .views import *

app_name = 'notification'

urlpatterns = [
    path('doctor-send-notification/', doctor_send_notification, name='doctor-send-notification'),
]


websocket_urlpatterns = [
    re_path(r'ws/notification/(?P<room_name>\w+)/$', consumers.NotificationConsumer.as_asgi()),
]