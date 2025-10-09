from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
import logging
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Message, Notification, MessageHistory

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


@receiver(pre_save, sender=Message)
def log_and_archive_before_update(sender, instance: Message, **kwargs):
	"""
	Before a Message is saved, if it's an update and the content changed,
	persist the old content to MessageHistory and mark the message as edited.
	"""
	if not instance.pk:
		# New message; nothing to archive
		return

	try:
		existing = Message.objects.get(pk=instance.pk)
	except Message.DoesNotExist:
		return

	if existing.content != instance.content:
		# Archive old content
		try:
			MessageHistory.objects.create(message=existing, old_content=existing.content)
		except Exception as e:
			logger.error(f"[signal] Failed to write history for message #{instance.pk}: {e}")
		# Mark as edited
		instance.edited = True

	# Also log the update attempt (only once per save)
	sender_user = getattr(instance, 'sender', None)
	receiver_user = getattr(instance, 'receiver', None)
	ts = timezone.now().isoformat()
	logger.info(
		f"[signal] Message #{instance.pk} pre-save at {ts} by {getattr(sender_user, 'email', sender_user)} -> {getattr(receiver_user, 'email', receiver_user)}"
	)


# Cleanup after user deletion (belt-and-suspenders beyond CASCADE FKs)
User = get_user_model()


@receiver(post_delete, sender=User)
def purge_user_messaging_data(sender, instance, **kwargs):
	"""
	Ensure all messaging artifacts for a deleted user are purged.
	Although FKs are CASCADE, this acts as a safety net and emits logs.
	"""
	try:
		# Delete messages where user is sender or receiver
		msg_qs = Message.objects.filter(Q(sender=instance) | Q(receiver=instance))
		msg_count = msg_qs.count()
		if msg_count:
			msg_qs.delete()

		# Delete notifications directly tied to the user
		notif_qs = Notification.objects.filter(user=instance)
		notif_count = notif_qs.count()
		if notif_count:
			notif_qs.delete()

		# MessageHistory rows tied to deleted Messages are cascaded; no direct link to User
		logger.info(
			f"[signal] Purged messaging data for deleted user #{getattr(instance, 'pk', instance)}: messages={msg_count}, notifications={notif_count}"
		)
	except Exception as e:
		logger.error(f"[signal] Failed to purge messaging data for deleted user #{getattr(instance, 'pk', instance)}: {e}")