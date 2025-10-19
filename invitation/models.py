from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class InvitationType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Invitation(models.Model):
    invitation_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    invitation_type = models.ForeignKey('InvitationType', on_delete=models.CASCADE)
    event_for = models.CharField(max_length=255, blank=False, null=False, help_text="Name of the person the event is for")
    event_date = models.DateTimeField(auto_now_add=False, auto_now=False,  help_text="Date and time of the event",null=False, blank=False)
    event_end_date = models.DateTimeField(null=True, blank=True)
    accepted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Invitation for {self.event_for} {self.invitation_type.name} at {self.event_date.date()}"
    class Meta:
        ordering = ['-event_date']


class invitedPerson(models.Model):
    invitation = models.ForeignKey('Invitation', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False, help_text="Name of the invited person")
    email = models.EmailField(blank=True, null=True, help_text="Email of the invited person")
    person_count = models.PositiveIntegerField(default=1, help_text="Number of people this invitation covers", null=True, blank=True)
    full_family = models.BooleanField(default=False, help_text="Does this invitation cover the full family?")
    rsvp = models.BooleanField(default=False, help_text="Has the invited person RSVP'd?")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the invited person")
    phone_number = PhoneNumberField(null=True, blank=True, help_text="Phone number of the invited person add the country code for example +1 for USA")


    def __str__(self):
        return f"{self.name} invited to {self.invitation.event_for}'s event"
    class Meta:
        ordering = ['name']