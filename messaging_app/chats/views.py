from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsParticipantOfConversation
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
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only return conversations for the logged-in user
        return Conversation.objects.filter(participants=self.request.user).distinct()

    def perform_create(self, serializer):
        conversation = serializer.save()
        # Ensure creator is included (in case client omitted)
        if not conversation.participants.filter(pk=self.request.user.pk).exists():
            conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    This is the Message ViewSet
    """
    queryset = Message.objects.select_related('conversation', 'sender').all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Messages from conversations user participates in
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if not conversation.participants.filter(pk=self.request.user.pk).exists():
            raise PermissionError("You are not a participant in this conversation")
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        # (Optional) restrict edits to original sender
        instance = self.get_object()
        if instance.sender != self.request.user:
            raise PermissionError("Only the sender can edit this message")
        serializer.save()