from django.urls import path
from . import views

urlpatterns = [
path('invitation/create',views.invitation_create, name="invitation_create"),
path('guest-management/<int:invitation_id>/', views.guest_management, name='guest_management'),
path('',views.redirect_view_to_main, name="redirect_to_main"),
path('load-themes/<int:type_id>/', views.load_themes, name='load_themes'),

#guest_managment
path('invitation/<int:invitation_id>/guest/<str:key>/delete/',views.delete_guest,name="delete_guest"),
path('invitation/<int:invitation_id>/guest/<str:guest_key>/edit/',views.edit_guest,name="edit_guest"),

#invitation_details
path('invitation/<int:invitation_id>/<str:guest_key>/', views.invitation_preview, name='invitation_preview'),
]
