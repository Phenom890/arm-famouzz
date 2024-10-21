from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from core.models import Contact


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('D', 'Do not Specify'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='D')

    def __str__(self):
        return self.user.username


class AdminReply(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(Contact, on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reply to {self.receiver.username}"