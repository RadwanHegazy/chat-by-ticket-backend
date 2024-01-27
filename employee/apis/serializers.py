from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from employee.models import User

class LoginSerializer (serializers.Serializer) :
    email = serializers.EmailField()
    password = serializers.CharField()
    tokens = {}

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        try : 
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"message":"invalid email"})
        
        if not user.check_password(password) : 
            raise serializers.ValidationError({"message":"invalid password"})
        
        self.tokens['token'] = str(RefreshToken.for_user(user).access_token)

        return attrs
    
class EmployeeSerializer (serializers.ModelSerializer) : 

    class Meta:
        model = User
        fields = ('id','full_name','picture',)
     
