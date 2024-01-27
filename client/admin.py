from django.contrib import admin
from .models import Ticket, Client

admin.site.register(Client)

class TicketPanel (admin.ModelAdmin) : 
    list_display = ['employee','client','is_done']


admin.site.register(Ticket, TicketPanel)
