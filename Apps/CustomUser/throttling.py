# from rest_framework.throttling import UserRateThrottle

# class FriendRequestThrottle(UserRateThrottle):
#     scope = 'friend_request'
    
#     def get_cache_key(self, request, view):
#         if not request.user.is_authenticated:
#             return None
#         return self.cache_format % {
#             'scope': self.scope,
#             'ident': request.user.pk
#         }


# from rest_framework.throttling import UserRateThrottle

# class FriendRequestThrottle(UserRateThrottle):
#     rate = '3/minute'

from rest_framework.throttling import UserRateThrottle

class FriendRequestThrottle(UserRateThrottle):
    scope = 'friend_request'


