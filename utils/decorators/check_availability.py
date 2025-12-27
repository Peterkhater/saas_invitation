from functools import wraps
from django.http import HttpResponseRedirect
from invitation.models import Invitation
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from datetime import timedelta
from datetime import datetime
from django.utils import timezone



def active_or_not(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        invitation_id = kwargs.get('invitation_id')
        invitation = get_object_or_404(Invitation, id=invitation_id)
        invitation_date_end = invitation.event_date + timedelta(days=7)

        now = timezone.now()  

        if now > invitation_date_end:
            passed = now - invitation_date_end
            print("Invitation expired", passed)
            invitation.active = False
            invitation.save()
            return redirect('profile')
        else:
            remaining = invitation_date_end - now
            print("Invitation still active for", remaining)

        return function(request, *args, **kwargs)

    return wrap
