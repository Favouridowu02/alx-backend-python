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
        fields = ["user_id", "first_name", "last_name", "email", "phone_number", "role", "created_at"]
        read_only_fields = ["user_id", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "conversation",
            "sender",
            "message_body",
            "sent_at",
            "updated_at",
        ]
        read_only_fields = ["message_id", "sent_at", "updated_at", "sender"]


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation including participants and nested messages."""
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
            "updated_at",
            "messages",
        ]
        read_only_fields = ["conversation_id", "created_at", "updated_at", "messages"]

    def validate_participants(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Conversation must include at least one participant")
        return value

    def create(self, validated_data):
        participants = validated_data.pop("participants", [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation

    def update(self, instance, validated_data):
        participants = validated_data.pop("participants", None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if participants is not None:
            instance.participants.set(participants)
        return instance