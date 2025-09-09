from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid


# Create your models here.
class User(AbstractBaseUser, models.Model):
    """
    This model is used to store the user details
    """

    class RoleChoices(models.TextChoices):
        ADMIN = "admin", "Admin"
        HOST = 'host', "Host"
        GUEST = "guest", "Guest"

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    # username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=128, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.GUEST,
        null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Conversation(models.Model):
    """
    This model is used to store the conversation details
    """
    conversation_id = models.UUIDField(primary_key=True)
    participants_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)