from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db import models
from django_jalali.db.models import jDateTimeField,jManager


class UserManager(BaseUserManager):
    def create_user(self, username=None, chat_id=None, password=None, **extra_fields):
        if not username and not chat_id:
            raise ValueError('Users must have username or chat_id')
        user = None
        if username and username == 'admin':
            user = self.model(username=username, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
        if chat_id:
            user = self.model(chat_id=chat_id, **extra_fields)
            user.set_unusable_password()
            user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        return self.create_user(username=username, password=password, **extra_fields)
    # Create your models here.


class User(PermissionsMixin, AbstractBaseUser):
    chat_id = models.CharField(unique=True, blank=True, null=True)
    username = models.CharField(unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username if self.username else str(self.chat_id)


class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='todos')
    title = models.CharField(max_length=125)
    is_completed = models.BooleanField(default=False)
    created_at = jDateTimeField(auto_now_add=True)
    objects = jManager()