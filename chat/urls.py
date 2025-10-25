from django.urls import path
from .views import (
    StartChatAPIView,
    SendMessageAPIView,
    ChatHistoryAPIView,
    EndChatAPIView
)

urlpatterns = [
    path("start/", StartChatAPIView.as_view(), name="start-chat"),
    path("<int:session_id>/send/", SendMessageAPIView.as_view(), name="send-message"),
    path("history/", ChatHistoryAPIView.as_view(), name="chat-history"),
    path("<int:session_id>/end/", EndChatAPIView.as_view(), name="end-chat"),
]
