from django.contrib import admin
from .models import Invitation, InvitationType, invitedPerson

admin.site.register(Invitation)
admin.site.register(InvitationType)
admin.site.register(invitedPerson)
# Register your models here.
