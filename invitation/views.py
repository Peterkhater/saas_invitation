from django.shortcuts import render
from .models import Invitation, InvitationType,Invitation_theme
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Guest
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.http import Http404
from event.models import Event

@login_required
def invitation_create(request):
    invitation_types = InvitationType.objects.all()

    if request.method == 'POST':
        invitation_type_id = request.POST.get('invitation_type')
        event_for = request.POST.get('event_for')
        event_date = request.POST.get('event_date')
        event_end_date = request.POST.get('event_end_date')
        notes = request.POST.get('notes')
        has_music = 'has_music' in request.POST 
        theme_id = request.POST.get('theme_') 

        print(f"invitation_type_id: {invitation_type_id}, event_for: {event_for}, event_date: {event_date}, event_end_date: {event_end_date}, notes: {notes}, has_music: {has_music}, theme_id: {theme_id}")


        if not invitation_type_id or not event_for or not event_date or not event_end_date or not theme_id:
            messages.error(request, "Please fill in all required fields.")
            return render(request,'invitation/invitation_create.html', {'invitation_types': invitation_types})
            

        request.session['invitation_data'] = {
            'invitation_owner': request.user.id,
            'invitation_type_id': invitation_type_id,
            'event_for': event_for,
            'event_date': event_date,
            'event_end_date': event_end_date,
            'notes': notes,
            'has_music_file': has_music, 
            'invitation_theme_id': theme_id,
        }
        
        return redirect('event_create')

    return render(request,'invitation/invitation_create.html', {'invitation_types': invitation_types})



@login_required
def guest_management(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    event = Event.objects.get(invitation=invitation)
    if request.user != invitation.invitation_owner:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    if request.method == 'POST':
        guest_name = request.POST.get('name')
        guest_email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        person_count = request.POST.get('person_count')
        full_family = True if request.POST.get('full_family') == 'on' else False
        notes = request.POST.get('notes')
        
        Guest.objects.create(
            invitation=invitation,
            name=guest_name,
            email=guest_email,
            phone_number=phone_number,
            person_count=person_count,
            full_family=full_family,
            notes=notes
        )
    
    # Get guests for this invitation and statistics
    guests = Guest.objects.filter(invitation=invitation)
    confirmed_guests = guests.filter(rsvp=True).count()
    pending_guests = guests.filter(rsvp=False).count()
    total_people = sum(guest.person_count for guest in guests)
    
    context = {
        'invitation': invitation,
        'guests': guests,
        'confirmed_guests': confirmed_guests,
        'pending_guests': pending_guests,
        'total_people': total_people,
        'event': event,
    }
    
    return render(request, 'invitation/guest_management.html', context)

def redirect_view_to_main(request):
    return redirect('home')





@require_POST
def delete_guest(request, invitation_id, key):
    invitation = get_object_or_404(Invitation, id=invitation_id)

    if request.user != invitation.invitation_owner:
        return HttpResponse('Permission denied', status=403)

    guest = get_object_or_404(Guest, invitation=invitation, guest_secret_key=key)
    guest.delete()
    return HttpResponse('deleted')



def edit_guest(request, invitation_id, guest_key):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    
    if request.user != invitation.invitation_owner:
        return HttpResponse('Permission denied', status=403)
    
    guest = get_object_or_404(Guest,invitation=invitation,guest_secret_key=guest_key)
    
    if request.method == "POST":
        # Update guest information
        guest.name = request.POST.get('name')
        guest.email = request.POST.get('email')
        guest.phone_number = request.POST.get('phone_number')
        guest.person_count = request.POST.get('person_count', 1)
        guest.full_family = request.POST.get('full_family') == 'on'
        guest.rsvp = request.POST.get('rsvp') == 'true'
        guest.notes = request.POST.get('notes')
        
        guest.save()
        messages.success(request, f"{guest.name}'s information has been updated successfully!")
        return redirect('guest_management', invitation_id=invitation_id)
    
    context = {
        'guest': guest,
        'invitation': invitation,
    }
    
    return render(request, 'invitation/guest_edit.html', context)



def load_themes(request, type_id):
    invitation_type = get_object_or_404(InvitationType, id=type_id)
    themes = Invitation_theme.objects.filter(invitation_type=invitation_type)
    
    themes_data = [
        {
            'id': theme.id,
            'name': theme.name,
            'description': theme.description,
            'premium': getattr(theme, 'premium', False),
            'image': {
                'src': request.build_absolute_uri(theme.image.url)
            } if theme.image else None,
            'features': getattr(theme, 'features', '').split(',') if getattr(theme, 'features', None) else []
        }
        for theme in themes
    ]
    
    return JsonResponse({'themes': themes_data})


def invitation_preview(request, invitation_id, guest_key):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    event = Event.objects.get(invitation=invitation)
    
    try:
        guest = Guest.objects.get(invitation=invitation, guest_secret_key=guest_key)
    except Guest.DoesNotExist:
        raise Http404("Guest not found for this invitation")

    person_range = range(1, guest.person_count + 1)
    template_render = invitation.invitation_theme.template_path

    context = {
        'invitation': invitation,
        'guest': guest,
        'event': event,
        'person_range': person_range, 
    }
    return render(request, template_render, context)