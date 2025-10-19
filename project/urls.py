
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('main/',include('core.urls')),
    path('',include('invitation.urls')),
    path('events/',include('event.urls')),
    path('gallery/',include('event_gallery.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
