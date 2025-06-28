# from django.contrib.auth.models import (
#     AbstractBaseUser,
#     BaseUserManager,
#     PermissionsMixin,
# )
# from django.db import models


# class UserAccountManager(BaseUserManager):
#     def create_user(self, username, email, password=None):
#         if not username:
#             raise ValueError("The Username field must be set")
#         if not email:
#             raise ValueError("The Email field must be set")
#         user = self.model(
#             username=username,
#             email=email,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None):
#         if not username:
#             raise ValueError("The Username field must be set")
#         if not email:
#             raise ValueError("The Email field must be set")
#         user = self.model(
#             username=username,
#             email=email,
#         )
#         user.set_password(password)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user


# class UserAccount(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     objects = UserAccountManager()

#     USERNAME_FIELD = "email"

#     def __str__(self):
#         return self.email
