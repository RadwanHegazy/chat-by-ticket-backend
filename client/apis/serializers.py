from ..models import Ticket, Client
from rest_framework import serializers
from django.contrib.humanize.templatetags import humanize

class ClientSerializer (serializers.ModelSerializer) : 
    class Meta:
        model = Client
        fields = "__all__"

class TicketSerializer (serializers.ModelSerializer) : 
    client = ClientSerializer()
    
    class Meta:
        model = Ticket
        fields = ('id','client','created_at','is_done')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        time = humanize.naturaltime(instance.created_at)
        data['created_at'] = time
        return data