from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class User (AbstractUser):
    username = None
    groups = None
    first_name = None
    last_name = None


    picture = models.ImageField(upload_to='pictures/',default='default.png')
    full_name = models.CharField(_('Full Name'),max_length=100)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name
    

class Employee (models.Model) :
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    picture  = models.ImageField(upload_to='employees-pics/',default='default.png')
    user = models.ForeignKey(User,null=True,blank=True,editable=False,on_delete=models.CASCADE)

    def __str__(self) : 
        return self.full_name
    

@receiver(post_save,sender = Employee)
def createAuthForEmp (created, instance, **kwargs) : 
    if created : 
        u = User.objects.create(
            full_name = instance.full_name,
            email = instance.email,
            picture = instance.picture,
        )

        u.set_password(instance.password)
        instance.password = ''
        
        instance.save()
        u.save()
        instance.user = u
        instance.save()