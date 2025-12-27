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
    image = models.ImageField( upload_to='invitation_type_image/', height_field=None, width_field=None, max_length=None, null=True, blank=True)
    tag = models.CharField(max_length=150, null=True,blank=True)
    def __str__(self):
        return self.name

def validate_guest_count(value):
    if value < 5:
        raise ValidationError("Invitation must have at least 5 guest.")


class Invitation_theme(models.Model):
    GENDARE =[('male','Male'),
           ('female','Female')]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True) 
    image = models.ImageField( upload_to='invitation_theme_image/', height_field=None, width_field=None, max_length=None, null=True, blank=True)
    tag = models.CharField(max_length=150, null=True,blank=True)
    invitation_type = models.ForeignKey(InvitationType, on_delete=models.CASCADE)
    html_code = models.TextField(null=True, blank=True)
    template_path = models.CharField(max_length=255, null=True, blank=True)
    gendare = models.CharField(max_length=20, choices=GENDARE, null=True, blank=True)

    def __str__(self):
        return f'{self.invitation_type} / {self.name}'
    
    def save(self, *args, **kwargs):
        if not self.template_path :
            self.template_path = ' '
        super().save(*args, **kwargs)


class Invitation(models.Model):
    invitation_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    invitation_type = models.ForeignKey(InvitationType, on_delete=models.CASCADE)
    invitation_theme = models.ForeignKey(Invitation_theme, on_delete=models.SET_NULL, null=True, blank=True)
    event_for = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    event_end_date = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    has_music_file = models.BooleanField(default=False)

    groom_name = models.CharField(null=True,blank=True)
    groom_info = models.TextField(blank=True, null=True)
    bride_name = models.CharField(blank=True, null=True)
    bride_info = models.TextField(null=True,blank=True)

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


class Rsvp(models.Model):
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, related_name="rsvps")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="rsvps")
    attending = models.BooleanField()
    person_count = models.PositiveIntegerField(default=1)
    message = models.TextField(blank=True, null=True)
    responded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RSVP by {self.guest.name} - {'Attending' if self.attending else 'Not Attending'}"

    class Meta:
        ordering = ['-responded_at']


