from django.shortcuts import render
from .models import Invitation, InvitationType
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Guest
from django.contrib import messages


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

        request.session['invitation_data'] = {
            'invitation_owner': request.user.id,
            'invitation_type_id': invitation_type_id,
            'event_for': event_for,
            'event_date': event_date,
            'event_end_date': event_end_date,
            'notes': notes,
            'has_music_file': has_music, 
        }

        return redirect('event_create')

    return render(request,'invitation/invitation_create.html', {'invitation_types': invitation_types})



@login_required
def guest_management(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    
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
    }
    
    return render(request, 'invitation/guest_management.html', context)