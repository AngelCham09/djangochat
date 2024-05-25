import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from .models import Room, Message, ChatImage
from django.contrib.auth.models import User
from .serializers import ChatImageSerializer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
     
        message = data['message']
        username = data['username']
        room = data['room']
        image_data = {'imageId': data.get('imageId')} if data.get('imageId') else {}

        if not message and not image_data.get('imageId'):
            # User site error handling (example using websockets)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_error',
                    'error': 'Please provide either a message or an image.'
                }
            )
        else:
            sync_to_async(self.save_message(username, room, message, **image_data))
            
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'room' : room,
                    'imageId': image_data.get('imageId')
                }
            )

    def chat_error(self, event):
        message_data = {
            'error_msg': event['error'],
        }
        self.send(text_data=json.dumps(message_data))


    def chat_message(self, event):
        message = event['message']
        username = event['username']
        imageId = event['imageId']

        message_data = {
            'message': message,
            'username': username,
            'image_url': None  # Default value if no image
        }

        if imageId:
            try:
                image = ChatImage.objects.get(pk=imageId)
                message_data['image_url'] = image.image.url
            except ChatImage.DoesNotExist:
                pass

        # Send message to WebSocket
        self.send(text_data=json.dumps(message_data))

 
    def save_message(self, username, room, message, imageId=None):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)
        if imageId:
            image = ChatImage.objects.get(pk=imageId)
            Message.objects.create(user=user, room=room, content=message, image=image)
        else:
            Message.objects.create(user=user, room=room, content=message)



    