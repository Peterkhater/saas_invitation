from django.db import models
from invitation.models import Invitation
from django.core.management.utils import get_random_secret_key

from django.utils.crypto import get_random_string


def generate_activation_token():
    return get_random_string(50)


class Event(models.Model):
    invitation = models.OneToOneField(Invitation, on_delete=models.CASCADE, related_name="event",blank=True, null=True, default=None)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gallery_event_featured = models.BooleanField(default=False)
    event_secret_key = models.CharField(max_length=100, blank=True, null=True)
    
    audio_file = models.FileField(upload_to='event_audios/', blank=True, null=True)
    beginningStory = models.TextField(blank=True, null=True)
    location_embed = models.TextField(blank=True, null=True)
    journeyStory = models.TextField(blank=True, null=True)
    proposalStory = models.TextField(blank=True, null=True)

    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-id']
    
    def save(self, *args, **kwargs):
        if not self.event_secret_key:
            self.event_secret_key = generate_activation_token()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('event_detail', args=[str(self.id)])

    


    def generate_qr_code(self, request=None):
        """Generate QR code with automatic URL detection"""
        if request:
            base_url = f"http://192.168.1.20"
        else:
            from django.conf import settings
            base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
        
        gallery_url = f"{base_url}/gallery/{self.invitation.id}/{self.event_secret_key}/"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(gallery_url)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        
        import base64
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        
        return f"data:image/png;base64,{qr_base64}"


    def get_qr_code_url(self, request=None):
        """Get the gallery URL with automatic host detection"""
        if request:
            # Use the request to build absolute URL
            from django.urls import reverse
            return request.build_absolute_uri(
                f'/gallery/{self.invitation.id}/{self.event_secret_key}/'
            )
        else:
            # Fallback
            from django.conf import settings
            base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
            return f"{base_url}/gallery/{self.invitation.id}/{self.event_secret_key}/"
