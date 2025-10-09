from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, MessageHistory
from rest_framework.test import APIClient
from rest_framework import status


class MessageHistorySignalTests(TestCase):
	def setUp(self):
		User = get_user_model()
		self.sender = User.objects.create_user(email="s@example.com", password="pass1234", first_name="S", last_name="User")
		self.receiver = User.objects.create_user(email="r@example.com", password="pass1234", first_name="R", last_name="User")

	def test_history_created_on_update_and_flag_set(self):
		msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello")
		self.assertFalse(msg.edited)

		# Update content triggers pre_save
		msg.content = "Hello world"
		msg.save()

		# Reload and assert edited flag set
		msg.refresh_from_db()
		self.assertTrue(msg.edited)

		# A history row should be created with old content
		history = MessageHistory.objects.filter(message=msg).order_by('-changed_at')
		self.assertEqual(history.count(), 1)
		self.assertEqual(history.first().old_content, "Hello")


class DeleteUserCascadeTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		User = get_user_model()
		self.sender = User.objects.create_user(email="del1@example.com", password="pass1234", first_name="D1", last_name="User")
		self.receiver = User.objects.create_user(email="del2@example.com", password="pass1234", first_name="D2", last_name="User")

	def test_delete_user_removes_messages_and_history(self):
		# Create a message and update it to generate history
		msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Original")
		msg.content = "Changed"; msg.save()
		self.assertEqual(Message.objects.count(), 1)
		self.assertEqual(MessageHistory.objects.count(), 1)

		# Auth as sender and delete account via API
		self.client.force_authenticate(user=self.sender)
		resp = self.client.delete('/api/users/delete/')
		self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.content)

		# Messages and histories tied to deleted user should be gone
		self.assertEqual(Message.objects.count(), 0)
		self.assertEqual(MessageHistory.objects.count(), 0)
