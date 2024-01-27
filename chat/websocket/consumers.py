from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from client.models import Ticket
from ..models import Chat, Message
import json
from ..serializer import MessageSerializer

class ChatConsumer (WebsocketConsumer) :

    def connect(self):
        self.user = self.scope['user']
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        
        try :
            self.ticket = Ticket.objects.get(id=self.ticket_id)
            
            if self.ticket.is_done: 
                self.close()
                return        
        
        except Ticket.DoesNotExist :
            self.close()
            return

        self.CHAT_GROUP = f'chat_{self.ticket_id}'
        
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.CHAT_GROUP,
            self.channel_name
        )

        try : 
            self.chat = Chat.objects.get(ticket=self.ticket)
        except Chat.DoesNotExist : 
            self.chat = Chat.objects.create(ticket=self.ticket)
            self.chat.save()

        messages = Message.objects.filter(chat=self.chat).order_by('id')
        messages = MessageSerializer(messages,many=True)
        
        async_to_sync(self.channel_layer.group_send)(
            self.CHAT_GROUP,
            {
                'type' : 'send_msg',
                'msgs' : messages.data
            }
        )


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.CHAT_GROUP,
            self.channel_name
        )


    def receive(self, text_data):
        message = json.loads(text_data)
        
        msg = Message.objects.create(
            body = message['message'],
            chat = Chat.objects.get(ticket=self.ticket)
        )

        msg.save()

        serializer = MessageSerializer(msg)

        async_to_sync(self.channel_layer.group_send)(
            self.CHAT_GROUP,
            {
                'type' : 'send_msg',
                'msgs' : serializer.data
            }
        )


    def send_msg (self, data) : 
        json_msgs = json.dumps(data['msgs'])
        self.send(text_data=json_msgs)