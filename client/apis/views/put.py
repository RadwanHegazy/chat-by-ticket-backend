from rest_framework import decorators, permissions, status
from rest_framework.response import Response
from client.models import Ticket

@decorators.api_view(['PUT'])
@decorators.permission_classes([permissions.IsAuthenticated])
def close_ticket (request,ticket_id) : 
    try :
        
        try : 
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({'message':"ticket not found"},status=status.HTTP_404_NOT_FOUND)

        ticket.is_done = True
        ticket.save()

        return Response({"message":"ticked closed successfully"},status=status.HTTP_200_OK)

    except Exception as error :
        return Response({
            'message' : f'an error accoured : {error}'
        },status=status.HTTP_400_BAD_REQUEST)