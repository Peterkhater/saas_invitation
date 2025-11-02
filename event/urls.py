from django.urls import path
from . import views

urlpatterns = [
    path('event/create', views.event_create, name='event_create'),
    path('event/event_activation_success', views.my_event_invitation_activate, name='my_event_invitation_activate'),

    path('event-management/<int:invitation_id>/', views.event_management, name='event_management'),
    # path('invitation/<int:pk>/', views.event_detail, name='event_detail'),

]
