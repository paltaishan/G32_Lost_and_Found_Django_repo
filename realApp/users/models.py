from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='default-profile.jpg')
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    USER_TYPES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    groups = models.ManyToManyField("auth.Group", related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField("auth.Permission", related_name="customuser_permissions", blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Only allow admin rights to specific user credentials
        special_admin_username = "adminuser"
        special_admin_password = "supersecret123"

        # If creating or updating a specific admin user
        if self.username == special_admin_username and self.check_password(special_admin_password):
            self.user_type = 'admin'
            self.is_superuser = True
            self.is_staff = True
        else:
            self.user_type = 'user'
            self.is_superuser = False
            self.is_staff = False

        super().save(*args, **kwargs)

    def is_admin(self):
        return self.user_type == 'admin'

    def is_normal_user(self):
        return self.user_type == 'user'










# from users.models import CustomUser
# user = CustomUser.objects.create_user(username='adminuser', password='supersecret123')
# user.save()
