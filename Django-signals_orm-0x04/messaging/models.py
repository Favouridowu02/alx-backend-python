from django.db import models
from django.conf import settings

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False, help_text="Indicates if the message content has been edited after creation")

    def __str__(self):
        return f"Message {self.id} at {self.created_at}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification {self.id} for User {self.user_id}"


class MessageHistory(models.Model):
    """
    Stores historical versions of Message content just before an update occurs.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-changed_at"]
        indexes = [
            models.Index(fields=["message", "changed_at"]),
        ]

    def __str__(self):
        return f"History for Msg {getattr(self.message, 'pk', '?')} at {self.changed_at}"