from rest_framework import serializers
from.models import User
from.validators import PasswordValidator


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'password')

    def create(self, validated_data):
        PasswordValidator.validate(self, validated_data["password"])
        user = User.objects.create(email=validated_data["email"],
                                   first_name=validated_data["first_name"],
                                   last_name=validated_data["last_name"])
        user.set_password(validated_data["password"])
        user.save()

        return user
