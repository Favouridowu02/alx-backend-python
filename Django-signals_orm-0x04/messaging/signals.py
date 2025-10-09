from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import logging

from .models import Message, Notification

logger = logging.getLogger('request_logger')


@receiver(post_save, sender=Message)
def notify_on_message_create(sender, instance: Message, created: bool, **kwargs):
	"""
	When a Message is created, automatically create a Notification for the receiver
	and log the event. Uses the `created` flag to avoid duplicate notifications on updates.
	"""
	if not created:
		return

	# Create a notification for the receiver
	try:
		Notification.objects.create(user=instance.receiver, message=instance)
	except Exception as e:
		logger.error(f"[signal] Failed to create notification for message #{instance.pk}: {e}")

	# Optional: log the event
	sender_user = getattr(instance, 'sender', None)
	receiver_user = getattr(instance, 'receiver', None)
	ts = timezone.now().isoformat()
	logger.info(
		f"[signal] New message #{instance.pk} at {ts} from {getattr(sender_user, 'email', sender_user)} to {getattr(receiver_user, 'email', receiver_user)}"
	)
