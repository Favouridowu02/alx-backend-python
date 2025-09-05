from django.db import models

# Create your models here.
class User(models.Model):
    class RoleChoices(models.TextChoices):
        ADMIN = "admin", "Admin"
        HOST = 'host', "Host"
        GUEST = "guest", "Guest"

    user_id = models.UUIDField(primary_key=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    email = models.EmailField(max_length=50, unique=True, null=False)
    # username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=128, null=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
        null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)   

class Conversion(models.Model):
    conversion_id = models.UUIDField(primary_key=True)
    participants_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)