from django.db import models
from event.models import Event
from invitation.models import Guest

class Gallery(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="gallery_images")
    image_owner = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='gallery_images/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.event.name} uploaded at {self.uploaded_at}"

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        ordering = ['-uploaded_at']