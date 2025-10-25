from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import FileExtensionValidator
from django.utils.crypto import get_random_string


def generate_activation_token():
    return get_random_string(50)

class InvitationType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

def validate_guest_count(value):
    if value < 5:
        raise ValidationError("Invitation must have at least 5 guest.")

class Invitation(models.Model):
    invitation_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    invitation_type = models.ForeignKey(InvitationType, on_delete=models.CASCADE)
    event_for = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    event_end_date = models.DateTimeField(null=True, blank=True)
    accepted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    invitation_persons_count = models.PositiveIntegerField()
    music_file = models.FileField(
        upload_to='invitations/music/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'flac'])]
    )
    has_music_file = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation for {self.event_for}"

    class Meta:
        ordering = ['-event_date']


class Guest(models.Model):
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, related_name="guests")
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    person_count = models.PositiveIntegerField(default=1)
    full_family = models.BooleanField(default=False)
    rsvp = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    guest_secret_key = models.CharField(max_length=255,null=True,blank=True)

    def save(self,*args, **kwargs):
        if not self.guest_secret_key:
            self.guest_secret_key = generate_activation_token()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} invited to {self.invitation.event_for}"

    class Meta:
        ordering = ['name']
