from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatSession, Message

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_staff"]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "text", "timestamp"]


class ChatSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    expert = UserSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ["id", "user", "expert", "is_active", "started_at", "ended_at", "messages"]
