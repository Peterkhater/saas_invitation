from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.payment_checkout, name='payment_checkout'),
    path('wishmoney/callback/', views.wishmoney_callback, name='wishmoney_callback'),
    path('success/', views.payment_success, name='payment_success'),
]
