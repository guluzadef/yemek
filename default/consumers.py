import json

from base_user.models import MyUser
from asgiref.sync import async_to_sync


from default.models import Notifications, Ordering
# from .mongo_client import Repo

from channels.generic.websocket import AsyncWebsocketConsumer


class UserSpecChat(AsyncWebsocketConsumer):
    # Connection to socket channel
    async def connect(self):
        self.room_name = self.scope['user'].id
        # print(self.room_name)
        self.room_group_name = 'notification_%s' % self.room_name
        # print(self.room_group_name)

        self.user = self.scope['user']
        # Join room group
        if self.user.username:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def receive(self, text_data):
        text_data = json.loads(text_data)
        from_user = MyUser.objects.filter(id=text_data['from_user']).last()
        to_user = MyUser.objects.filter(id=text_data['to_user']).last()
        activity_type = text_data['activity_type']
        try:
            ordering_id = Ordering.objects.filter(id=text_data['ordering_id']).last()
        except:
            ordering_id =False
        if ordering_id == False or ordering_id.status == False:
            Notifications.objects.create(
                from_user=from_user,
                to_user=to_user,
                activity_type=activity_type
            )
            await self.channel_layer.group_send(
                "notification_%s" % to_user.id,
                {"type": "send_notification",
                 "data": {
                     "message": activity_type
                 }})
            try:
                if activity_type != '2':
                    ordering_id.status = True
                    ordering_id.save()
                else:
                    ordering_id.expire = True
                    ordering_id.save()
            except:
                pass
    async def send_notification(self, event):
        data = event['data']
        # print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )