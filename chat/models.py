from django.db import models
from client.models import Ticket
from uuid import uuid4

class Chat (models.Model) : 
    ticket = models.ForeignKey(Ticket,related_name='ticket_for_chat',on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True,db_index=True,editable=False,default=uuid4)

    def __str__(self) -> str:
        return f"{self.ticket.employee.full_name} | {self.ticket.client.full_name}"

class Message (models.Model) : 
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self) -> str:
        return self.body