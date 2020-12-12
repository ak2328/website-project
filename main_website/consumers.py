# from django.contrib.auth import get_user_model
from users.models import MyUser
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message
import pdb
from .models import Notification,ChannelOnlineCount
# from channels import Group

# User = get_user_model()   

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        # pdb.set_trace()
        reciever_id = data['reciever_id']

        messages = Message().last_10_messages(self.room_group_name)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)


    def new_message(self, data):
        author = data['from']
        print(author)
        author_user = MyUser.objects.filter(mobile=author)[0]


        reciever = self.room_group_name.replace('_'+str(author_user.id)+'_','').replace('_' + str(author_user.id)+'_','')
        reciever = reciever.replace('_','')
        reciever = reciever.replace('chat','')

        # try:
        count = ChannelOnlineCount.objects.get(author_reciever_string = self.room_group_name).count
        print('count')
        print(count)

        old_message_recieved = Message.objects.filter(
            author=MyUser.objects.filter(id=reciever)[0],
            author_reciever_string=self.room_group_name,
            reciever = self.scope["user"].id,
        ).count()
        old_message_sent = Message.objects.filter(
            author=self.scope["user"].id,
            author_reciever_string=self.room_group_name,
            reciever = MyUser.objects.filter(id=reciever)[0],
        ).count()
        if old_message_recieved == 0 and old_message_sent == 1:
            # if old_message_sent == 1:
            print('sent 1')
            self.disconnect()

        if count == 1:
            message = Message.objects.create(
                author=author_user,
                author_reciever_string=self.room_group_name,              
                content=data['message'],
                reciever = MyUser.objects.filter(id=reciever)[0],
                seen_status = False
            )            
            Notification.objects.create(
                reciever = MyUser.objects.get(id=reciever),
                author = author_user,
                author_reciever_string=self.room_group_name,              
                count=1)
            # Notification.objects.filter(
            #     reciever = MyUser.objects.get(id=reciever),
            #     author = author_user,
            #     author_reciever_string=self.room_group_name).delete()
        else:
            message = Message.objects.create(
                author=author_user,
                author_reciever_string=self.room_group_name,              
                content=data['message'],
                reciever = MyUser.objects.filter(id=reciever)[0],
                seen_status = True
            )            
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        print('getattr(self.channel_layer, self.channel_name, 0)')
        print(getattr(self.channel_layer, self.channel_name, 0))

        return self.send_chat_message(content)


    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result


    def message_to_json(self, message):
        return {
            'author': message.author.mobile,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):


        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        reciever = self.room_group_name.replace('_'+str(self.scope["user"].id)+'_','').replace('_' + str(self.scope["user"].id)+'_','')
        reciever = reciever.replace('_','')
        reciever = reciever.replace('chat','')


        old_message_recieved = Message.objects.filter(
            author=MyUser.objects.filter(id=reciever)[0],
            author_reciever_string=self.room_group_name,
            reciever = self.scope["user"].id,
        ).count()
        old_message_sent = Message.objects.filter(
            author=self.scope["user"].id,
            author_reciever_string=self.room_group_name,
            reciever = MyUser.objects.filter(id=reciever)[0],
        ).count()

        try:
            channel_count = ChannelOnlineCount.objects.get(author_reciever_string=self.room_group_name)
            channel_count.count += 1
            channel_count.save()
        except:
            self.scope["session"][self.room_name] = 1
            ChannelOnlineCount.objects.create(author_reciever_string=self.room_group_name, count=1)
        print(old_message_recieved)
        print('old_message_recieved')
        print(old_message_sent)
        if old_message_recieved == 0 and old_message_sent == 1:
            # if old_message_sent == 1:
            print('sent 1')
            self.disconnect()

        else:

            Message.objects.filter(
                author=MyUser.objects.filter(id=reciever)[0],
                author_reciever_string=self.room_group_name,
                reciever = self.scope["user"].id,
                seen_status = False
            ).update(seen_status=True)


            Notification.objects.filter(
                reciever = MyUser.objects.get(id=self.scope["user"].id),
                author = MyUser.objects.filter(id=reciever)[0],
                author_reciever_string=self.room_group_name).delete()

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()



    def disconnect(self, close_code):

        channel_count = ChannelOnlineCount.objects.get(author_reciever_string = self.room_group_name)
        channel_count.count -= 1

        if channel_count.count == 0:
            channel_count.delete()
        else:
            channel_count.save()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):

        data = json.loads(text_data)        
        self.commands[data['command']](self, data)
        

    def send_chat_message(self, message):   
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))




import json
from channels.generic.websocket import WebsocketConsumer

class NotificationSocketHome(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["user"].id
        self.room_group_name = 'notif_%s' % self.room_name

        # Join room group
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

    def receive(self, text_data):
        pass

    def recieve_group_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(
             text_data=json.dumps({
            'message': message
        }))

class ChatGroupConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message().last_10_messages('all')
        messages = messages[::-1]
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = MyUser.objects.filter(mobile=author)[0]
        message = Message.objects.create(
            author=author_user,
            author_reciever_string='all',              
            content=data['message'])

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)


    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result


    def message_to_json(self, message):
        return {
            'author': message.author.mobile,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = 'all'
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

    def receive(self, text_data):
        data = json.loads(text_data)        
        self.commands[data['command']](self, data)
        

    def send_chat_message(self, message):   
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))



# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatAuditorium(WebsocketConsumer):
    def connect(self):
        # pdb.set_trace()
        self.room_name = self.scope['url_route']['kwargs']['organization_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # pdb.set_trace()
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        owner = False
        try:
            text_data_json['owner']
            owner = True
        except:
            owner = False

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'owner':owner
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        # pdb.set_trace()
        message = event['message']
        owner = 'true'
        if event['owner']:
            owner = 'true'
        else:
            owner = 'false'
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'owner_status': owner
        }))

from datetime import datetime
from .models import Analytics
import string 
import random 

class AnalyticsConsumer(WebsocketConsumer):
    def connect(self):
        N = 10;
        self.scope["session"]["random_session_id"] = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
        self.scope["session"].save()                 
        self.accept()

    def disconnect(self, close_code):
        analytics = Analytics.objects.filter(user_id = self.scope["session"]['_auth_user_id'],random_string = self.scope["session"]['random_session_id'],end_time = None)
        for analytic in analytics:
            # anlytic.last()      
            analytic.end_time = datetime.now()
            analytic.save()


    # Receive message from WebSocket
    def receive(self, text_data):
        
        text_data =  json.loads(text_data)

        
        Analytics.objects.create(
            page_name = text_data['pagename'],
            company_name = text_data['company_name'],
            stall_name = text_data['stall_url'],
            start_time = datetime.now(),
            user_id = MyUser.objects.get(id = self.scope["session"]['_auth_user_id']),
            random_string = self.scope["session"]['random_session_id']
        )
        self.send(text_data=json.dumps({
                    'success': 'success'
        }))
