from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Conversation, Message
import uuid

class ChatAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="user1@example.com", password="pass1234", first_name="U1", last_name="Test") if hasattr(User.objects, 'create_user') else User.objects.create(email="user1@example.com", password_hash="x", first_name="U1", last_name="Test")
        self.user2 = User.objects.create_user(email="user2@example.com", password="pass1234", first_name="U2", last_name="Test") if hasattr(User.objects, 'create_user') else User.objects.create(email="user2@example.com", password_hash="x", first_name="U2", last_name="Test")
        self.client = APIClient()

    def authenticate(self, user):
        # If using JWT normally you'd obtain token; for test simplicity force auth
        self.client.force_authenticate(user=user)

    def test_conversation_creation_and_auto_add_creator(self):
        self.authenticate(self.user1)
        url = '/api/conversations/'
        payload = {"participants": [str(self.user2.user_id)]}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        convo_id = response.data['conversation_id']
        convo = Conversation.objects.get(conversation_id=convo_id)
        self.assertIn(self.user1, convo.participants.all())
        self.assertIn(self.user2, convo.participants.all())

    def test_conversation_list_requires_auth(self):
        url = '/api/conversations/'
        response = self.client.get(url)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_message_create_by_participant(self):
        self.authenticate(self.user1)
        convo = Conversation.objects.create()
        convo.participants.add(self.user1, self.user2)
        url = '/api/messages/'
        payload = {"conversation": str(convo.conversation_id), "message_body": "Hello"}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(response.data['message_body'], 'Hello')

    def test_message_create_forbidden_for_non_participant(self):
        self.authenticate(self.user1)
        convo = Conversation.objects.create()
        convo.participants.add(self.user2)  # user1 NOT added
        url = '/api/messages/'
        payload = {"conversation": str(convo.conversation_id), "message_body": "Hidden"}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_conversation_list_shows_only_participating(self):
        self.authenticate(self.user1)
        c1 = Conversation.objects.create(); c1.participants.add(self.user1)
        c2 = Conversation.objects.create(); c2.participants.add(self.user2)
        url = '/api/conversations/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = {item['conversation_id'] for item in response.data}
        self.assertIn(str(c1.conversation_id), returned_ids)
        self.assertNotIn(str(c2.conversation_id), returned_ids)
