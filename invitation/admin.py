from django.contrib import admin
from .models import Invitation, InvitationType, Guest

admin.site.register(Invitation)
admin.site.register(InvitationType)
admin.site.register(Guest)
