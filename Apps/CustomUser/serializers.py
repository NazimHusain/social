from rest_framework import serializers
from typing import Any, Union
from Apps.CustomUser import models as UserModels
from config.excetions import CustomValidation

class UserLoginSerializer(serializers.Serializer):
    """Serializer for User's login."""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self: 'UserLoginSerializer', attrs: dict) -> Union[dict, CustomValidation]:
        username = attrs["username"]
        password = attrs["password"]
        self.user = UserModels.User.objects.filter(email=username, is_active=True).first()
        if self.user and self.user.check_password(password):
            return attrs
        else:
            raise CustomValidation("Invalid Credentials", 400)
        

class UsersSerializer(serializers.ModelSerializer):
    role  = serializers.SerializerMethodField()
    profilePic = serializers.SerializerMethodField()
    class Meta:
        model = UserModels.User

        fields = ('id','first_name','last_name','email','profilePic','role')

    def get_role(self: 'UsersSerializer', user: Any) -> Union[None, dict]:
        try:
            return user.role.name if user.role else None
        except Exception:
            return None

    def get_profilePic(self: 'UsersSerializer', user: Any) -> Union[None, dict]:
        request = self.context["request"]
        try:
            return {
                "file": request.build_absolute_uri(user.profilePic.file.url),
                "id": user.profilePic.id,
            }
        except Exception:
            return None



class CreatedRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModels.FriendRequest
        fields = ['receiver']



class FriendSerializer(serializers.ModelSerializer):
    sender = UsersSerializer()
    class Meta:
        model = UserModels.FriendRequest
        fields = ['sender']



# class FriendRequestSerializer(serializers.ModelSerializer):
#     sender = UserSerializer(read_only=True)
#     receiver = UserSerializer()

#     class Meta:
#         model = FriendRequest
#         fields = ['id', 'sender', 'receiver', 'created_at', 'status']


  


# class FriendRequestSerializer(serializers.ModelSerializer):
#     sender = UserSerializer(read_only=True)
#     receiver = UserSerializer(read_only=True)

#     class Meta:
#         model = FriendRequest
#         fields = ['id', 'sender', 'receiver', 'created_at', 'status']