from rest_framework import status, decorators
from employee.apis.serializers import LoginSerializer
from rest_framework.response import Response


@decorators.api_view(['POST'])
def LoginView (request): 
    try : 
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid() : 
            return Response(serializer.tokens,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as error :
        return Response({
            'message' : f"an error accured : {error}"
        },status=status.HTTP_400_BAD_REQUEST)
    