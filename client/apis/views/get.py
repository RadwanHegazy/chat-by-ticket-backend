from rest_framework import decorators, permissions, status
from rest_framework.response import Response
from ...models import Ticket, Employee
from ..serializers import TicketSerializer

@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
def get_tickets (request) : 
    try :
        employee = Employee.objects.get(user=request.user)
        query = Ticket.objects.filter(employee=employee,is_done=False).order_by('created_at')
        serializer = TicketSerializer(query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as error :
        return Response({
            'message' : f'an error accoured : {error}'
        },status=status.HTTP_400_BAD_REQUEST)
    
@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.AllowAny])
def get_ticket_info (request,ticket_id) : 
    try :
        
        try : 
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({'message':"ticket not found"},status=status.HTTP_404_NOT_FOUND)

        if ticket.is_done : 
            return Response({'message':"ticket not found"},status=status.HTTP_404_NOT_FOUND)

        serialzier = TicketSerializer(ticket)
        return Response(serialzier.data,status=status.HTTP_200_OK)

    except Exception as error :
        return Response({
            'message' : f'an error accoured : {error}'
        },status=status.HTTP_400_BAD_REQUEST)