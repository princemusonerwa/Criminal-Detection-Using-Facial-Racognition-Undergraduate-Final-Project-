from django.db import models
from detect.models import Person
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from PIL import Image

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, names, phone, gender, dob, password = None ):
        if not email:
            raise ValueError("Email is required!")
        if not names:
            raise ValueError("Names are required!")
        if not phone:
            raise ValueError("Phone number is required!")
        if not gender:
            raise ValueError("Gender is required!")
        user = self.model(
            email = self.normalize_email(email),
            names = names,
            phone = phone,
            gender = gender,
            dob=dob,
            password  = password
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, names, phone, gender, dob, password = None):
        user = self.create_user(
            email = email,
            names=names,
            phone=phone,
            gender=gender, 
            dob=dob,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(Person, AbstractBaseUser, PermissionsMixin):
    date_joined = models.DateTimeField(auto_now_add=True) 
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_securityOfficer = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["names", 'phone','gender', 'dob']

    def __str__(self):
        return self.names

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="images/profile_pics")

    def __str__(self):
        return f'{self.user.names} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 and img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)