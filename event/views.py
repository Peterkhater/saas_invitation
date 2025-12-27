from django.shortcuts import render
from django.shortcuts import redirect
from invitation.models import Invitation, InvitationType, Invitation_theme,Rsvp
from .models import Event
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib.auth.decorators import login_required
from payment.models import Payment
from django.http import HttpResponseForbidden

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
            
        if request.user.is_superuser:
            return redirect('my_event_invitation_activate')
        else:
            payment = Payment.objects.create(
                user=request.user,
                amount=20,
                status='PENDING'
            )

            request.session['payment_id'] = payment.id
            return redirect('payment_checkout')


    return render(request, 'event/event_create.html')




# @login_required
# def my_event_invitation_activate(request):
#     invitation_data = request.session.get('invitation_data')
#     event_data = request.session.get('event_data')
    
#     if not invitation_data or not event_data:
#         return redirect('invitation_create')

#     try:
        
#         user = get_object_or_404(User, id=invitation_data['invitation_owner'])
#         invitation_type = get_object_or_404(InvitationType, id=invitation_data['invitation_type_id'])
#         invitation_theme = get_object_or_404(Invitation_theme, id=invitation_data['invitation_theme_id'])
        
#         # Create the Invitation
#         invitation = Invitation.objects.create(
#             invitation_owner=user,
#             invitation_type=invitation_type,
#             event_for=invitation_data['event_for'],
#             event_date=invitation_data['event_date'],
#             event_end_date=invitation_data['event_end_date'],
#             invitation_theme=invitation_theme,
#             notes=invitation_data.get('notes', ''),
#             has_music_file=invitation_data.get('has_music_file', False),
#         )

#         # Create the Event
#         event = Event.objects.create(
#             invitation=invitation,
#             name=event_data['name'],
#             location=event_data['location'],
#             description=event_data['description'],
#             gallery_event_featured=event_data['gallery_event_featured']
#         )

#         # Clear session after success
#         for key in ['invitation_data', 'event_data']:
#             request.session.pop(key, None)

#     except Exception as e:
#         print(f"Error creating Invitation or Event: {e}")
#         return render(request, 'event/event_activation_error.html', {'error': str(e)})

#     return render(request, 'event/event_activation_success.html', {'invitation': invitation, 'event': event})

@login_required
def my_event_invitation_activate(request):

    if not request.user.is_superuser:
        payment_id = request.session.get('payment_id')

        if not payment_id:
            return HttpResponseForbidden("Payment required")

    invitation_data = request.session.get('invitation_data')
    event_data = request.session.get('event_data')
    
    if not invitation_data or not event_data:
        return redirect('invitation_create')

    try:
        user = get_object_or_404(User, id=invitation_data['invitation_owner'])
        invitation_type = get_object_or_404(
            InvitationType, id=invitation_data['invitation_type_id']
        )
        invitation_theme = get_object_or_404(
            Invitation_theme, id=invitation_data['invitation_theme_id']
        )

        invitation = Invitation.objects.create(
            invitation_owner=user,
            invitation_type=invitation_type,
            event_for=invitation_data['event_for'],
            event_date=invitation_data['event_date'],
            event_end_date=invitation_data['event_end_date'],
            invitation_theme=invitation_theme,
            notes=invitation_data.get('notes', ''),
            has_music_file=invitation_data.get('has_music_file', False),
        )

        event = Event.objects.create(
            invitation=invitation,
            name=event_data['name'],
            location=event_data['location'],
            description=event_data['description'],
            gallery_event_featured=event_data['gallery_event_featured']
        )

        # 🧹 clear session
        for key in ['invitation_data', 'event_data', 'payment_id']:
            request.session.pop(key, None)

    except Exception as e:
        return render(request, 'event/event_activation_error.html', {'error': str(e)})

    return render(
        request,
        'event/event_activation_success.html',
        {'invitation': invitation, 'event': event}
    )


def event_management(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    event = get_object_or_404(Event, invitation=invitation)
    

    if request.user != invitation.invitation_owner:
        return redirect('home')
    
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == "Event_Information":
            event.name = request.POST.get('event_name')
            invitation.event_for = request.POST.get('event_for')
            event_date_str = request.POST.get('event_date')
            if event_date_str:
                try:
                    invitation.event_date = datetime.fromisoformat(event_date_str)
                    invitation.save()
                except ValueError:
                    print("Invalid ISO datetime format:", event_date_str)

            event.location = request.POST.get('location')
            event.description = request.POST.get('description')
            event.save()
            invitation.save()
            return redirect('event_management', invitation_id=invitation.id)

        elif form_type == "Love_Stories":
            event.beginningStory = request.POST.get('beginningStory')
            event.journeyStory = request.POST.get('journeyStory') 
            event.proposalStory = request.POST.get('proposalStory')
            event.save()
            return redirect('event_management', invitation_id=invitation.id)

        elif form_type == "Invitation_Settings":
            invitation.has_music_file = 'has_music_file' in request.POST
            invitation.active = 'active' in request.POST
            invitation_music_file = request.FILES.get('audio_file')

            if invitation_music_file:
                event.audio_file = invitation_music_file
                event.save()
                
            invitation.save()
            return redirect('event_management', invitation_id=invitation.id)

    return render(request, 'event/event_managment.html', {'invitation': invitation, 'event': event})