from django.urls import path
from Apps.CustomUser import views

urlpatterns = [
    path("register/", (views.SignUp.as_view())),
    path("login/", views.UserLogin.as_view()),
    path("logout/", views.UserLogout.as_view()),
    path("users/list/", views.UserList.as_view()),
    path('send/request/', views.SendFriendRequest.as_view(), name='send-request'),
    path('request/<int:pk>/', views.AcceptRejectRequestView.as_view(), name='accept-reject-request'),
    path('friends/', views.FriendsList.as_view(), name='friends-list'),
    path('friends/pending/', views.PendingFriendsList.as_view(), name='pending-friends-list'),
    # path("post/<int:postId>/", views.PostDetails.as_view()),
    # path("comment/", views.CommentAPIView.as_view()),
]



# urlpatterns = [
#     path('friend-request/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
#     path('friend-request/<int:pk>/<str:action>/', AcceptRejectFriendRequestView.as_view(), name='accept-reject-friend-request'),
#     path('friends/', ListFriendsView.as_view(), name='list-friends'),
#     path('friend-requests/pending/', ListPendingFriendRequestsView.as_view(), name='list-pending-friend-requests'),
# ]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('send_friend_request/', views.SendFriendRequestView.as_view(), name='send_friend_request'),
#     path('accept_friend_request/', views.AcceptFriendRequestView.as_view(), name='accept_friend_request'),
#     path('reject_friend_request/', views.RejectFriendRequestView.as_view(), name='reject_friend_request'),
#     path('list_friends/', views.ListFriendsView.as_view(), name='list_friends'),
#     path('list_pending_friend_requests/', views.ListPendingFriendRequestsView.as_view(), name='list_pending_friend_requests'),
# ]




# from django.urls import path
# from .views import FriendRequestListCreateView, FriendRequestUpdateView, FriendListView, PendingFriendRequestsView

# urlpatterns = [
#     path('requests/', FriendRequestListCreateView.as_view(), name='friend-request-list-create'),
#     path('requests/<int:pk>/', FriendRequestUpdateView.as_view(), name='friend-request-update'),
#     path('friends/', FriendListView.as_view(), name='friend-list'),
#     path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
# ]
