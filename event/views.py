from django.shortcuts import render
from django.shortcuts import redirect
from invitation.models import Invitation, InvitationType
from .models import Event
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def event_create(request):
    invitation_data = request.session.get('invitation_data')
    if not invitation_data:
        return redirect('invitation_create')

    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        location = request.POST.get('location')
        description = request.POST.get('description')
        gallery_featured = 'gallery_event_featured' in request.POST

        request.session['event_data'] = {
            'name': event_name,
            'location': location,
            'description': description,
            'gallery_event_featured': gallery_featured
        }

        return redirect('my_event_invitation_activate')

    return render(request, 'event/event_create.html')



def my_event_invitation_activate(request):
    invitation_data = request.session.get('invitation_data')
    event_data = request.session.get('event_data')

    if not invitation_data or not event_data:
        return redirect('invitation_create')

    try:
        
        user = get_object_or_404(User, id=invitation_data['invitation_owner'])
        invitation_type = get_object_or_404(InvitationType, id=invitation_data['invitation_type_id'])

        # Create the Invitation
        invitation = Invitation.objects.create(
            invitation_owner=user,
            invitation_type=invitation_type,
            event_for=invitation_data['event_for'],
            event_date=invitation_data['event_date'],
            event_end_date=invitation_data['event_end_date'],
            notes=invitation_data.get('notes', ''),
            has_music_file=invitation_data.get('has_music_file', False)
        )

        # Create the Event
        event = Event.objects.create(
            invitation=invitation,
            name=event_data['name'],
            location=event_data['location'],
            description=event_data['description'],
            gallery_event_featured=event_data['gallery_event_featured']
        )

        # Clear session after success
        for key in ['invitation_data', 'event_data']:
            request.session.pop(key, None)

    except Exception as e:
        print(f"Error creating Invitation or Event: {e}")
        return render(request, 'event/event_activation_error.html', {'error': str(e)})

    return render(request, 'event/event_activation_success.html', {'invitation': invitation, 'event': event})