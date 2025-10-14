from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from .models import Message

class IsOwner(permissions.BasePermission):
    """Allow access only to object owners (objects with a 'user' attribute)."""
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user", None) == request.user


class IsParticipantOfConversation(permissions.BasePermission):
    """Allow access only to authenticated users that are participants in the related conversation.

    Supported object types:
    - Conversation: must expose participants via `participants` (ManyToMany) or single `participants_id` FK
    - Message: must expose a related `conversation` with participants or a sender reference
    """
    def has_permission(self, request, view):
        # Global level: user must be authenticated for any access
        return bool(request.user and request.user.is_authenticated)

    def _is_participant(self, user, obj):
        """Internal helper to determine if user participates in the object's conversation context."""
        if user is None or not user.is_authenticated:
            return False

        # Direct conversation object cases
        if hasattr(obj, 'participants'):
            try:
                participants_qs = getattr(obj, 'participants').all()
                return participants_qs.filter(pk=user.pk).exists()
            except Exception:
                pass

        # Single participant FK (legacy) named participants_id
        if hasattr(obj, 'participants_id'):
            participant_user = getattr(obj, 'participants_id', None)
            if participant_user is not None:
                return participant_user == user

        # Message referencing a conversation via `conversation` attr
        if hasattr(obj, 'conversation'):
            conversation = getattr(obj, 'conversation')
            return self._is_participant(user, conversation)

        # Message with sender attribute (fallback) – ensure sender is the user
        for sender_attr in ['sender', 'sender_id']:
            if hasattr(obj, sender_attr) and getattr(obj, sender_attr) == user:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False
        # For modifying methods, verify conversation membership via conversation_id
        if request.method in ("PUT", "PATCH", "DELETE"):
            conv_id = None
            try:
                data = request.data
                conv_id = data.get('conversation_id') or data.get('conversation')
            except Exception:
                conv_id = None

            if not conv_id:
                conv_id = getattr(obj, 'conversation_id', None)
            if not conv_id:
                conv = getattr(obj, 'conversation', None)
                conv_id = getattr(conv, 'conversation_id', None) if conv is not None else None

            if not conv_id:
                raise PermissionDenied(detail="Missing conversation identifier; access denied.")

            try:
                allowed = Message.objects.filter(
                    conversation_id=conv_id,
                    conversation__participants__pk=request.user.pk,
                ).exists()
            except Exception:
                allowed = False

            if not allowed:
                raise PermissionDenied(detail="You are not a participant of this conversation or message.")

            return True

        is_participant = self._is_participant(request.user, obj)
        if request.method in permissions.SAFE_METHODS:
            return is_participant
        return is_participant