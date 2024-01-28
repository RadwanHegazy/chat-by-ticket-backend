from django.urls import path
from .views import get, put, create


urlpatterns = [
    path('tickets/all/',get.get_tickets),
    path('ticket/<str:ticket_id>/',get.get_ticket_info),
    path('close-ticket/<str:ticket_id>/',put.close_ticket),
    path('create/',create.CreateClient),
]