import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder

from comments.services.broadcast import COMMENTS_GROUP


class CommentConsumer(AsyncWebsocketConsumer):
    """Read-only feed: clients connect to receive newly created comments in real time."""

    async def connect(self):
        await self.channel_layer.group_add(COMMENTS_GROUP, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(COMMENTS_GROUP, self.channel_name)

    async def comment_created(self, event):
        await self.send(text_data=json.dumps(event["comment"], cls=DjangoJSONEncoder))
