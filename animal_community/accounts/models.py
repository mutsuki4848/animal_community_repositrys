from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
from django.conf import settings

class Pet(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=(('1', 'オス'), ('2', 'メス')), default=1)
    picture = models.ImageField(upload_to='pet_pictures/', blank=True, null=True)
    genre = models.CharField(
    max_length=10,
    choices=(('1', '犬'), ('2', '猫'), ('3', '鳥類'), ('4', '齧歯類'), ('5', '爬虫類')),
    default='1',
)
    breed = models.CharField(max_length=100, blank=True)  # 品種
    characteristic = models.TextField(blank=True)  # 性格や特徴
    
    def __str__(self):
        return self.name

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='picture/', blank=True, null=True)
    favorite_animals = models.CharField(max_length=255, blank=True)  # 好きな動物のためのフィールド
    pet = models.ManyToManyField(Pet, blank=True, related_name='users') #飼っているペットのためのフィールド
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        
class UserActivateTokensManager(models.Manager):
    
    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
            token = token,
            expired_at__gte=datetime.now()
        ).first()
        user = user_activate_token.user
        user.is_active = True
        user.save()
        
class UserActivateTokens(models.Model):
    
    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField()
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )
    
    objects = UserActivateTokensManager()
    
    class Meta:
        db_table = 'user_activate_tokens'
        
@receiver(post_save, sender=Users)
def publish_token(sender, instance, **kwargs):
    user_activate_token = UserActivateTokens.objects.create(
        user = instance, token=str(uuid4()), expired_at = datetime.now() + timedelta(days=1)
    )    
    print(f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}')
