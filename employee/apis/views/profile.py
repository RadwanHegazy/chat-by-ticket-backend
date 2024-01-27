from rest_framework import status, decorators, permissions
from rest_framework.response import Response

@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
def ProfileView (requset) : 
    try : 
        user = requset.user
        return Response({
            "id" : user.id,
            "full_name" : user.full_name,
            "picture" : user.picture.url,
        })
    
    except Exception as error :
        return Response({
            "message" : f"an error accured : {error}"
        },status=status.HTTP_400_BAD_REQUEST)