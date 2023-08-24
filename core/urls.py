from django.urls import path, re_path
from .views import *

app_name = 'core'


urlpatterns = [
    path('', IndexView, name='index'),
    path('parent_dashboard/', ParentDashboard, name='parent-dashboard'),
    path('parent-profile-update/', parent_profile_settings, name='parent-profile-update'),
    path('parent-dashboard/change-password/', dashboard_change_password, name='dashboard-change-password'),
    path('child-profile/<uuid>/', child_profile, name='child-profile'),
    path('child-profile-update/<uuid>/', child_profile_update, name='child-profile-update'),

    path('child/immunization-detail/<uuid:uuid>/', child_immunization_detail, name='child-immunization-detail'),

    path('doctor-dashboard/', doctor_dashboard, name='doctor-dashboard'),
    path('doctor-children-assigned/', doctor_children_assigned, name='doctor-children-assigned'),
    path('doctor-appointments/', doctor_appintments, name='doctor-appointments'),
    path('doctor-profile-settings/', doctor_profile_update, name='doctor-profile-update'),


    path('create-child/', create_child, name='create-child'),
    path('child-profile-update/<uuid>/', child_profile_update, name='child-profile-update'),
    path('child-profile-delete/<uuid:uuid>/', delete_child, name='child-delete'),

    path('clients/', clients, name='clients'),

    path('terms-and-conditions/', terms_and_conditions, name='terms-and-conditions'),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),
]

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notification/(?P<room_name>\w+)/$', consumers.NotificationConsumer.as_asgi()),
]