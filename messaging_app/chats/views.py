from django.shortcuts import render
from rest_framework import viewsets
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


class MessageViewSet(viewsets.ModelViewSet):
    """
    This is the Message ViewSet
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer