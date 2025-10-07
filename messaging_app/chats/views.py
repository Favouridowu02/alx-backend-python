from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    MessageSerializer,
)

from .models import (
    User,
    Conversation,
    Message,
)

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    """
    This is the Conversation ViewSet
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Only return conversations for the logged-in user
        return Conversation.objects.filter(participants_id=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    This is the Message ViewSet
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Only return messages for the logged-in user
        return Message.objects.filter(sender_id=self.request.user)