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
    It handles nested relationship 
    """
    class Meta:
        model = Conversation
        fields = "__all__"
        read_only_field = ["conversation_id", "participants_id"]

class MessageSerializer(serializers.ModelSerializer):
    """
    This is the Serializer for Message Model
    It handles nested relationships
    """
    class Meta:
        model = Message
        fields = "__all__"
        read_only_field = ["sender_id", "message_id"]