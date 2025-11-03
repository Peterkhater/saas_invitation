from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('category/<int:id>',views.category_invitation,name='category'),
    path('theme/<int:id>/',views.theme_preview,name='theme_preview'),
    path('accounts/profile/', views.profile, name='profile'),
    path('guide/', views.guidelance, name='guidelance'),

]
