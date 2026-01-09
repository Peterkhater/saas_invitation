from django.shortcuts import render
from .models import Invitation, InvitationType,Invitation_theme, Rsvp
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Guest
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.http import Http404
from event.models import Event
# mail imports
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from utils.decorators.check_availability import active_or_not
from datetime import timedelta
from datetime import datetime
from django.utils import timezone

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

        
        if not invitation_type_id or not event_for or not event_date or not theme_id:
            messages.error(request, "Please fill in all required fields.")
            return render(request,'invitation/invitation_create.html', {'invitation_types': invitation_types})
            

        request.session['invitation_data'] = {
            'invitation_owner': request.user.id,
            'invitation_type_id': invitation_type_id,
            'event_for': event_for,
            'event_date': event_date,
            'event_end_date': event_end_date or None,
            'notes': notes,
            'has_music_file': has_music, 
            'invitation_theme_id': theme_id,
        }
        
        return redirect('event_create')

    return render(request,'invitation/invitation_create.html', {'invitation_types': invitation_types})


# @active_or_not
@login_required
def guest_management(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    event = Event.objects.get(invitation=invitation)
    rsvp = Rsvp.objects.filter(invitation=invitation)
    invitation_date_end = invitation.event_date + timedelta(days=7)

    now = timezone.now()  

        

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

        print(invitation_date_end, now)
        if now > invitation_date_end:
            messages.error(request, "Cannot add guest. Invitation has expired.")
            return redirect('guest_management', invitation_id=invitation_id)

        Guest.objects.create(
            invitation=invitation,
            name=guest_name,
            email=guest_email,
            phone_number=phone_number,
            person_count=person_count,
            full_family=full_family,
            notes=notes
        )
        messages.success(request, f"Guest {guest_name} has been added successfully!")
        return redirect('guest_management', invitation_id=invitation_id)
    
    # Get guests for this invitation and statistics
    guests = Guest.objects.filter(invitation=invitation)
    confirmed_guests = guests.filter(rsvp=True).count()
    pending_guests = guests.filter(rsvp=False).count()
    total_people = sum(guest.person_count for guest in guests)
    
    sum_of_comming_people = 0
    for guest in rsvp:
        if guest.attending:
            sum_of_comming_people += guest.person_count
    
    
    context = {
        'invitation': invitation,
        'guests': guests,
        'confirmed_guests': confirmed_guests,
        'pending_guests': pending_guests,
        'total_people': total_people,
        'event': event,
        'sum_of_comming_people': sum_of_comming_people,
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


@active_or_not
def edit_guest(request, invitation_id, guest_key):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    
    if request.user != invitation.invitation_owner:
        return HttpResponse('Permission denied', status=403)

    if not invitation.active:
        raise Http404("No MyModel matches the given query.")
    
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
    guest = get_object_or_404(Guest, invitation=invitation, guest_secret_key=guest_key)

    # if not invitation.active:
    #     return redirect("home")

    if not invitation.active:
        raise Http404("No MyModel matches the given query.")

    if request.method == 'POST':
        person_count = request.POST.get('guests_count')
        attending_value = request.POST.get('attending')
        rsvp = True if attending_value == 'yes' else False
        guest.rsvp = rsvp
        notes = request.POST.get('message')
        guest.save()


        if not Rsvp.objects.filter(guest=guest, invitation=invitation).exists():
            Rsvp.objects.create(
                guest=guest,
                invitation=invitation,
                attending=rsvp,
                person_count=person_count,
                message=notes
            )
            return redirect('invitation_preview', invitation_id=invitation.id, guest_key=guest.guest_secret_key)
    
    

    person_range = range(1, guest.person_count + 1)
    template_render = invitation.invitation_theme.template_path
    if not template_render:
        template_render = invitation.invitation_theme.html_code

    context = {
        'invitation': invitation,
        'guest': guest,
        'event': event,
        'person_range': person_range, 
    }
    return render(request, template_render, context)



def send_mail_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id)

    if not invitation.active:
        messages.error(request, "Invitation is not active. Cannot send emails.")
        return redirect('guest_management', invitation_id=invitation_id)

    if request.user != invitation.invitation_owner:
        return HttpResponse('Permission denied', status=403)

    guests = invitation.guests.all()
    
    if not guests.exists():
        messages.warning(request, "No guests found to send invitations to.")
        return redirect('guest_management', invitation_id=invitation_id)
    
    email_count = 0
    for guest in guests:
        if guest.rsvp:
            pass 
        elif guest.email:  # Only send if guest has an email
            subject = f"You're Invited to {invitation.event_for}!"
            html_message = render_to_string('invitation/emails/email_invitation.html', {
                'invitation': invitation,
                'guest': guest,
                'invitation_link': request.build_absolute_uri(
                    f"/invitation/{invitation.id}/{guest.guest_secret_key}/" 
                )
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = guest.email

            try:
                send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
                email_count += 1
            except Exception as e:
                print(f"Failed to send email to {guest.email}: {e}")
    
    messages.success(request, f"Successfully sent {email_count} invitation emails!")
    return redirect('guest_management', invitation_id=invitation_id)



def send_single_reminder_email(request, invitation_id, guest_key):
    invitation = get_object_or_404(Invitation,id=invitation_id)
    guest = get_object_or_404(Guest, invitation=invitation, guest_secret_key=guest_key)

    if not invitation.active:
        messages.error(request, "Invitation is not active. Cannot send emails.")
        return redirect('guest_management', invitation_id=invitation_id)

    if request.user != invitation.invitation_owner:
        return HttpResponse('Permission denied', status=403)
    
    if not guest.email:
        messages.error(request, f"No email found for guest {guest.name}.")
        return redirect('guest_management', invitation_id=invitation_id)
    
    subject = f"Reminder: You're Invited to {invitation.event_for}!"
    html_message = render_to_string('invitation/emails/email_invitation.html', {
        'invitation': invitation,
        'guest': guest,
        'invitation_link': request.build_absolute_uri(
            f"/invitation/{invitation.id}/{guest.guest_secret_key}/" 
        )
    })
    plain_message = strip_tags(html_message)

    try:
        send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [guest.email], html_message=html_message)
        print(f"Reminder email sent to {guest.name} at {guest.email}.")
        messages.success(request, f"Reminder email sent to {guest.name} at {guest.email}.")
    except Exception as e:
        messages.error(request, f"Failed to send email to {guest.email}: {e}")
        print(f"Failed to send email to {guest.email}: {e}")

    messages.success(request, f"Successfully sent invitation email!")
    return redirect('guest_management', invitation_id=invitation_id)



# from utils.whatsapp import send_whatsapp_message
# def send_invitation_whatsapp(request, invitation_id):
#     invitation = get_object_or_404(Invitation, id=invitation_id)
#     guests = invitation.guests.all()

#     sent_to = []

#     for guest in guests:
#         link = request.build_absolute_uri(
#             f'/invitation/{invitation.id}/{guest.guest_secret_key}/'
#         )
#         send_whatsapp_message(
#             to_number=str(guest.phone_number),  # ✅ convert to string
#             message=f"🎉 You’re invited! View your invitation: {link}"
#         )
#         sent_to.append(str(guest.phone_number))

#     return JsonResponse({"status": "success", "sent": len(sent_to), "recipients": sent_to})


# def send_invitation_whatsapp(request, invitation_id):
#     invitation = get_object_or_404(Invitation, id=invitation_id)
#     guests = invitation.guests.all()

#     sent_count = 0
#     for guest in guests:
#         link = request.build_absolute_uri(
#             f'/invitation/{invitation.id}/{guest.guest_secret_key}/'
#         )
#         message = f"🎉 You’re invited! View your invitation here: {link}"

#         response = send_whatsapp_message(
#             to_number=guest.phone_number,
#             message=message
#         )

#         if response.get("messages"):
#             sent_count += 1
        

#     return JsonResponse({"status": "success", "sent": sent_count})

import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from invitation.models import Invitation
from utils.whatsapp import send_whatsapp_message


def send_invitation_whatsapp(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    guests = invitation.guests.all()

    sent_count = 0
    recipients = []

    for guest in guests:
        link = request.build_absolute_uri(
            f'/invitation/{invitation.id}/{guest.guest_secret_key}/'
        )

        phone = str(guest.phone_number).strip()
        if not phone.startswith('+'):
            phone = '+' + phone

        response = send_whatsapp_message(
            to_number=phone,
            guest_name=guest.name,
            event_name=invitation.event.name,
            event_date=str(invitation.event_date),
            invitation_link=link,
        )
        print(response)

       
        if response.get("messages"):
            sent_count += 1
            recipients.append(phone)

    return JsonResponse({
        "status": "success",
        "sent": sent_count,
        "recipients": recipients
    })
