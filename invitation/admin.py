from django.contrib import admin
from .models import Invitation, InvitationType, Guest, Invitation_theme

admin.site.register(Invitation)
admin.site.register(InvitationType)
admin.site.register(Invitation_theme)
admin.site.register(Guest)
