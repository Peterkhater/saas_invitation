from django.db import models
from invitation.models import Invitation

class Event(models.Model):
    invitation = models.OneToOneField(Invitation, on_delete=models.CASCADE, related_name="event",blank=True, null=True, default=None)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gallery_event_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-id']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('event_detail', args=[str(self.id)])
