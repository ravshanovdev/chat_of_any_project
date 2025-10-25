from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ChatSession, Message
from .serializers import ChatSessionSerializer, MessageSerializer
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class StartChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        expert = User.objects.filter(role="expert").first()

        if not expert:
            return Response({"message": "there's not available expert, please wait.!"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        session = ChatSession.objects.create(user=user, expert=expert)
        serializer = ChatSessionSerializer(session)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        try:

            session = ChatSession.objects.get(id=session_id, is_active=True)
        except ChatSession.DoesNotExist:
            return Response(
                {"error": "Bunday faol chat sessiya topilmadi"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        is_farmer_invalid = user.role == "farmer" and user != session.user
        is_expert_invalid = user.role == "expert" and user != session.expert

        if is_farmer_invalid or is_expert_invalid:
            return Response({"message": "You do not have permission to join this chat!"}, status=403)

        text = request.data.get("text")

        if not text:
            return Response({"error": "text kiritish majburiy.!"}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            session=session,
            sender=request.user,
            text=text,
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == "expert":
            sessions = ChatSession.objects.filter(expert=user).order_by("-started_at")
        else:
            sessions = ChatSession.objects.filter(user=user).order_by("-started_at")

        serializer = ChatSessionSerializer(sessions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class EndChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, is_active=True)
        except ChatSession.DoesNotExist:
            return Response(
                {"error": "Bunday faol chat sessiya topilmadi"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = request.user

        is_farmer_invalid = user.role == "farmer" and user != session.user
        is_expert_invalid = user.role == "expert" and user != session.expert

        if is_farmer_invalid or is_expert_invalid:
            return Response({"message": "You do not have permission to end this chat!"}, status=403)

        session.is_active = False
        session.ended_at = timezone.now()
        session.save()
        return Response({"status": "Chat yakunlandi"}, status=200)




