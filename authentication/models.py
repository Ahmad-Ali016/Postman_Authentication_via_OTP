from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# This stores the extra info
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)  # Added null/blank
    phone = models.CharField(max_length=15, null=True, blank=True)  # Added null/blank

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.code}"