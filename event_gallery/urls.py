from django.urls import path
from . import views
urlpatterns = [
path('<int:id>/<str:key>/',views.gallery_show,name="event_gallery_images_show"),
]