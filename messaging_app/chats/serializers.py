#!/usr/bin/python3
"""
This file contains the serializers for the chats app
"""

from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    This is the Serializer for Users Model
    """
    class Meta:
        model = User
        fields = "__all__"
        read_only_field = ["user_id"]

class ConversationSerializer(serializers.ModelSerializer):
    """
    This is the Serializer for Conversation Model
    It handles nested relationship and includes messages
    """
    participants = serializers.CharField(source='participants_id.email', read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = "__all__"
        read_only_field = ["conversation_id", "participants_id"]

    def get_messages(self, obj):
        messages = Message.objects.filter(conversation_id=obj.conversation_id)
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        # Example validation: ensure at least one participant
        if not data.get('participants_id'):
            raise serializers.ValidationError("Conversation must have a participant.")
        return data

class MessageSerializer(serializers.ModelSerializer):
    """
    This is the Serializer for Message Model
    It handles nested relationships
    """
    class Meta:
        model = Message
        fields = "__all__"
        read_only_field = ["sender_id", "message_id"]