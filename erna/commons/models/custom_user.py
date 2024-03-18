'''
customary user
'''
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin


class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser, PermissionsMixin):
    objects = CustomUserManager()

    class Meta:
        app_label = 'commons'

    def __str__(self):
        return self.username
    
    def to_dict(self):
        return {
            'user_id': self.id,
            'username': self.username,
        }
    
    