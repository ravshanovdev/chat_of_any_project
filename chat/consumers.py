import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f"chat_{self.session_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        from .models import ChatSession, Message  # ✅ lokal import

        try:
            data = json.loads(text_data)
            sender_id = data.get("sender_id")
            message = data.get("message")

            if not sender_id or not message:
                await self.send(json.dumps({"error": "Invalid payload"}))
                return

            session = await self.get_session(self.session_id)
            sender = await self.get_user(sender_id)
            await self.save_message(session, sender, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender_id": sender_id
                }
            )
        except json.JSONDecodeError:
            await self.send(json.dumps({"error": "Invalid JSON format"}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"]
        }))

    @staticmethod
    async def get_user(user_id):
        User = get_user_model()
        return await User.objects.aget(id=user_id)

    @staticmethod
    async def get_session(session_id):
        from .models import ChatSession  # ✅ lokal import
        return await ChatSession.objects.aget(id=session_id)

    @staticmethod
    async def save_message(session, sender, message):
        from .models import Message  # ✅ lokal import
        await Message.objects.acreate(session=session, sender=sender, text=message)
