from django.db import models
from Apps.Helpers import models as coreModels
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from Apps.CustomUser.managers import CustomUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    """Model for saving basic user info."""

    email = models.EmailField("email address", unique=True, null=True, blank=True)
    username = models.EmailField("username", unique=True)  
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    role = models.ForeignKey(
        coreModels.DropdownValues, null=True, blank=True, on_delete=models.PROTECT
    )
    profilePic = models.ForeignKey(
        coreModels.FileUpload,
        null=True,
        blank=True,
        related_name="user_profile_pic",
        on_delete=models.PROTECT,
    )
    USERNAME_FIELD = "username"
    objects = CustomUserManager()

    def __str__(self: "User") -> str:
        return str(self.username)
    




class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')

    class Meta:
        unique_together = ('sender', 'receiver')

    def clean(self):
        if self.sender == self.receiver:
            raise ValidationError("You cannot send a friend request to yourself.")
        
        # if FriendRequest.objects.filter(from_user=self.from_user, created_at__gte=timezone.now()-timezone.timedelta(minutes=1)).count() >= 3:
        #     raise ValidationError("You cannot send more than 3 friend requests within a minute.")








