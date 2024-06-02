from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotAcceptable
from django.db import DatabaseError
from Apps.CustomUser import models as UserModels
from rest_framework.authtoken.models import Token
from Apps.Helpers import models as coreModels
from django.contrib.auth import login, logout
from Apps.CustomUser import serializers 
from django.db.models import Q
from config.pagination import ApiPaginator
from Apps.CustomUser.throttling import FriendRequestThrottle


from django.core.cache import cache
from django.utils import timezone
from rest_framework import permissions, status

# from .serializers import CreateFriendRequestSerializer
# from .serializers import FriendRequestSerializer, CreateFriendRequestSerializer, UserSerializer

pagination_class = ApiPaginator()
# Create your views here.
class SignUp(APIView):
    """Api for Register User."""

    permission_classes = ()
    authentication_classes = ()

    def post(self: "SignUp", request: Request, *args: any, **kwargs: any) -> Response:
        data = request.data
        try:
            if data.get("email"):
                user = UserModels.User.objects.create_user(
                    username=data.get("email"),
                    email=data.get("email"),
                    password=data.get("password")) 
                
            token, _ = Token.objects.get_or_create(user=user)
            if data.get("first_name"):
                user.first_name = data.get("first_name")
            if data.get("last_name"):
                user.last_name = data.get("last_name")

            if data.get("role"):
                user.role = coreModels.DropdownValues.objects.get(slug="user-roles")
            if data.get("profilePic"):
                user.profilePic = coreModels.FileUpload.objects.get(id=data.get("profilePic"))
            user.save()

            return Response({"key": token.key}, 201)
        except DatabaseError:
            raise NotAcceptable("Username already exists")
        except Exception as e:
            print(str(e))
            raise NotAcceptable("User could not be created, check the data")
        

class UserLogin(APIView):
    """Api for Login User.
    username(str) - username of user
    password(str) - password of user
    """

    permission_classes = []

    def post(self: "UserLogin", request: Request, version: str) -> Response:
        data = request.data
        try:
            data["username"]
        except Exception:
            try:
                data["username"] = data["email"]
            except Exception:
                return Response(
                    {
                        "response": "User created but cannot login, please try login manually."
                    },
                    400,
                )
        data["password"] = data.get("password")
        serialized = serializers.UserLoginSerializer(data=data)
        if serialized.is_valid():
            user = serialized.user
            login(request, user)
            Token.objects.filter(user=user).delete()
            token, _ = Token.objects.get_or_create(user=user)
            data, success_code = {
                "key": token.key,
                "role": user.role.slug if user.role.slug else None,
                }, 200
            return Response(data, success_code)
        return Response(serialized.errors)
    
class UserLogout(APIView):
    """APi for logout"""

    def post(self: "UserLogout", request: Request, version: str) -> Response:
        request.auth.delete()
        logout(request)
        data = {"response": "Log out Successfully"}
        return Response(data=data, status=200)
    
class UserList(APIView):
    def get(self: "UserList", request:Request,version:str) -> Response:
        search = request.GET.get('search')
        QuerySet = UserModels.User.objects.all()
        if search:
            QuerySet = QuerySet.filter(Q(first_name__icontains=search)|Q(last_name__icontains=search) | Q(email__contains=search))
        
        result_page = pagination_class.paginate_queryset(QuerySet, request)
        serialized = serializers.UsersSerializer(result_page, many=True, context={"request": request})
        return pagination_class.get_paginated_response(serialized.data)
        





class SendFriendRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        serializer = serializers.CreatedRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            receiver_id = serializer.validated_data['receiver'].id
            if UserModels.FriendRequest.objects.filter(sender=user,receiver_id=receiver_id, status = 'pending').exists():
                return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(sender=user)
            return Response({'success':'Friend request Sent Successfully.','receiver_id':receiver_id},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class AcceptRejectRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, version, pk):
        action = request.GET.get('action')
        try:
            friend_request = UserModels.FriendRequest.objects.get(id=pk, receiver=request.user, status='pending')
            if action == 'accept':
                friend_request.status = 'accepted'
                friend_request.save()
                return Response({'status': 'Friend request accepted'}, status=status.HTTP_200_OK)
            elif action == 'reject':
                friend_request.status = 'rejected'
                friend_request.save()
                return Response({'status': 'Friend request rejected'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        except UserModels.FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found or already processed'}, status=status.HTTP_404_NOT_FOUND)


class FriendsList(APIView):
    def get(self: "FriendsList", request:Request,version:str) -> Response:
        user = self.request.user
        QuerySet = UserModels.FriendRequest.objects.filter(receiver=user, status='accepted')
        serialized = serializers.FriendSerializer(QuerySet, many=True, context={"request": request})
        return Response(serialized.data, status=status.HTTP_200_OK)
     
        
class PendingFriendsList(APIView):
    def get(self: "PendingFriendsList", request:Request,version:str) -> Response:
        user = self.request.user
        QuerySet = UserModels.FriendRequest.objects.filter(receiver=user, status='pending')
        serialized = serializers.FriendSerializer(QuerySet, many=True, context={"request": request})
        return Response(serialized.data, status=status.HTTP_200_OK)




