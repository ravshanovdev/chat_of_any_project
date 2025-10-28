from django.conf import settings
from django.db import models


class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_sessions', on_delete=models.CASCADE)
    expert = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='expert_sessions', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)


class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
