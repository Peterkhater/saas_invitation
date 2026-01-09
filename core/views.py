from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from event.models import Event
from invitation.models import Invitation
from django.utils import timezone
from invitation.models import InvitationType,Invitation_theme
from django.http import HttpResponse
from django.utils.safestring import mark_safe

def home(request):
    invitation_categorys = InvitationType.objects.all()
    return render(request, 'main/home.html',{'invitation_category':invitation_categorys})

def category_invitation(request, id):
    invitation_type = get_object_or_404(InvitationType, id=id)
    invitation_themes_list = get_list_or_404(Invitation_theme, invitation_type=invitation_type)
    return render(request, 'main/category_invitation.html', {
        'invitation_themes_list': invitation_themes_list,
        'invitation_type': invitation_type,
    })

def theme_preview(request,id):
    theme = get_object_or_404(Invitation_theme, id=id)
    theme_html_path = theme.template_path.strip()

    if theme.html_code:
        return HttpResponse(mark_safe(theme.html_code))
    elif theme_html_path:
        return render(request,theme_html_path,{"theme":theme})
    else:
        return HttpResponse("no Design")




def profile(request):
    if not request.user.is_authenticated:
        return redirect('home')

    invitations = Invitation.objects.filter(invitation_owner=request.user)
    events = Event.objects.filter(invitation__in=invitations)
    total_guests = 0
    

    for invitation in invitations:
        total_guests+=invitation.guests.count()

    now = timezone.now()

    active_events = Invitation.objects.filter(event_end_date__gt=now)
    upcoming_events = Invitation.objects.filter(event_end_date__lt=now)
    
    # peter
    active_events = Invitation.objects.filter(event_end_date__lt=now)

    return render(request, 'user/profile.html', {
        "user_events": events,
        "invitation": invitations,
        "event_count": events.count(),
        "total_guests_invited": total_guests,
        "active_events":active_events.count(),
        "upcoming_events":upcoming_events.count(),
    })


def guidelance(request):
    return render(request, 'main/guide.html')

# def mysaas(request):
#     return render(request, 'main/my_saas.html')

