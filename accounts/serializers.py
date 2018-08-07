from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    '''
    serializers for serializing User model
    '''
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True,
    )

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email',
                  'password',)

