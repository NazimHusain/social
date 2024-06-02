from django.contrib import admin
from Apps.CustomUser import models as User


# Register your models here.


class AdminUser(admin.ModelAdmin):
    list_display = ("id","email", "username","role","profilePic")
admin.site.register(User.User, AdminUser)

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ("id","sender", "receiver","created_at","status")
admin.site.register(User.FriendRequest, FriendRequestAdmin)
