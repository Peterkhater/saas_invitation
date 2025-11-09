from django.shortcuts import render, redirect
from invitation.models import Invitation
from django.shortcuts import get_object_or_404
from event.models import Event
from .models import Gallery
import qrcode



def gallery_show(request, id,key):
    invitation = get_object_or_404(Invitation, id=id)

    if not invitation.event.gallery_event_featured:
        #we can add the logic to add this feature and pay for it later
        return redirect('home')
    
    if invitation.event.event_secret_key != key:
        return redirect('home')

    if request.method == 'POST':
        images = request.FILES.getlist('image')
        caption = request.POST.get('caption')
        guest_name = request.POST.get('guest_name')
        print(images)
        for image in images:
            Gallery.objects.create(
                event=invitation.event,
                image=image,
                image_owner=guest_name,
                caption=caption
            )
        return redirect('event_gallery_images_show', id=invitation.id, key=key)

    event = get_object_or_404(Event, invitation=invitation)
    gallery_images = Gallery.objects.filter(event=event)
    contributers = set()
    for image in gallery_images:
        contributers.add(image.image_owner)

    context = {
        'gallery_images': gallery_images,
        'total_photos': gallery_images.count(),
        'event': event,
        'total_contributors': len(contributers),
        
    
    }
    

    return render(request, 'event_gallery/gallery_show.html', context)



