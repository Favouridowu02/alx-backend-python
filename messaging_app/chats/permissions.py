from rest_framework import permissions

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

        # Single participant FK (current simplified Conversation model) named participants_id
        if hasattr(obj, 'participants_id'):
            participant_user = getattr(obj, 'participants_id', None)
            if participant_user is not None:
                return participant_user == user

        # Message referencing a conversation via `conversation` attr
        if hasattr(obj, 'conversation'):
            conversation = getattr(obj, 'conversation')
            # Recurse once on conversation
            return self._is_participant(user, conversation)

        # Message with sender attribute (fallback) – ensure sender is the user
        for sender_attr in ['sender', 'sender_id']:
            if hasattr(obj, sender_attr):
                if getattr(obj, sender_attr) == user:
                    return True

        return False

    def has_object_permission(self, request, view, obj):
        # Must still be authenticated
        if not (request.user and request.user.is_authenticated):
            return False

        is_participant = self._is_participant(request.user, obj)

        # Read-only safe methods allowed for participants only
        if request.method in permissions.SAFE_METHODS:
            return is_participant

        # Mutating actions (POST, PUT, PATCH, DELETE) only for participants
        return is_participant