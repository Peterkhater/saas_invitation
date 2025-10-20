from django.urls import path
from . import views

urlpatterns = [
path('invitation/create',views.invitation_create, name="invitation_create"),
  path('guest-management/<int:invitation_id>/', views.guest_management, name='guest_management'),
]
