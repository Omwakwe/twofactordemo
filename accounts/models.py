from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserAccountManager(BaseUserManager):
    def create_user(self, user_name, password=None):
        if not email:
            raise ValueError('Email must be set!')
        user = self.model(user_name=user_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password):
        user = self.create_user(user_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, user_name_):
        return self.get(user_name=user_name_)
# using AbstractBaseUser so as to customize to add email
class User(AbstractBaseUser):
    """
            Custom user class
    """
    user_name = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70,blank=True, null= True)
    two_factor_active = models.BooleanField(default=False)

    email_confirmed = models.BooleanField(default=False)
    
    activation_code = models.CharField(max_length=100)

    USERNAME_FIELD = 'user_name'
    objects = UserAccountManager()

    def natural_key(self):
        return self.user_name


    def __str__(self):
        return self.first_name + ' ' + self.second_name

    class META:
        app_label = 'accounts'
