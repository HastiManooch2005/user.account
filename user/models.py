from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self,username, password,fullname):
        if not username:
            raise ValueError("Users must have phone or email")
        if not password:
            raise ValueError("Users must have password")
        user = self.model(username=username,fullname=fullname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, password,fullname):
        if not username:
            raise ValueError("Users must have phone or email")
        if not password:
            raise ValueError("Users must have password")
        user = self.model(username=username, fullname=fullname)
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(verbose_name='Username', max_length=100, unique=True)
    fullname = models.CharField(verbose_name='Full name', max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

