from django.db import models
from django.utils import timezone


class Invite(models.Model):
    code = models.CharField(max_length=50, unique=True)
    date_last_access = models.DateTimeField(null=True, blank=True)
    sent_invite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code}"


class MenuType(models.Model):
    menu_name = models.CharField(max_length=100)

    def __str__(self):
        return self.menu_name


class InvitedPerson(models.Model):
    invite = models.ForeignKey(Invite, on_delete=models.CASCADE, related_name='people')
    family_name = models.CharField(max_length=100, null=True, blank=True)
    given_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.family_name} {self.given_name}".strip()


class Response(models.Model):
    invite = models.OneToOneField(Invite, on_delete=models.CASCADE, related_name='response')
    is_coming = models.BooleanField(null=True, blank=True)
    date_of_response = models.DateTimeField(default=timezone.now)
    message = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Response for {self.invite.code}"


class ConfirmedPerson(models.Model):
    invite = models.ForeignKey(Invite, on_delete=models.CASCADE, related_name='confirmed_people')
    full_name = models.CharField(max_length=200)
    menu_type = models.ForeignKey(MenuType, on_delete=models.SET_NULL, null=True, related_name='confirmed_people')

    def __str__(self):
        return f"{self.full_name} ({self.menu_type})"
