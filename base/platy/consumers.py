import json
import secrets

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from django.contrib.auth.models import User
from django.db.models import Q
from platy.models import Friends, DirectMessages



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print(self.scope['url_route'])

        l_sender = self.scope['url_route']['kwargs']['sender']
        l_target = self.scope['url_route']['kwargs']['target']
        
        l_sender_user = User.objects.get(username=l_sender)
        l_target_user = User.objects.get(username=l_target)

        friendship = Friends.objects.filter(
            (Q(req_sender_id=l_sender_user.id) & Q(req_receiver_id=l_target_user.id)) | 
            (Q(req_sender_id=l_target_user.id) & Q(req_receiver_id=l_sender_user.id))
        )[0]

        print(friendship.id)

        # self.room_group_naWme = 'testing'
        
        self.room_group_name = str(friendship.id).strip()
        print('Will be added to group', self.room_group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )


        self.accept()


        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'The connection has been established.'
            })
        )

    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        sender = text_data_json['chat_sender']
        target = text_data_json['chat_target'] 
        message = text_data_json['message']
      
        print(f'From {sender}, to {target} ==>')
        print('WS Message:', message)


        l_sender_user = User.objects.get(username=sender)
        l_target_user = User.objects.get(username=target)
        new_msg = DirectMessages(
            text_content=message,
            msg_receiver_id=l_target_user.id,
            msg_sender_id=l_sender_user.id
        )
        new_msg.save()


        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        # self.send(text_data=json.dumps({
            # 'type': 'chat',
            # 'message': message
        # }))

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))


