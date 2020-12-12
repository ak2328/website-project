from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, mobile, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not mobile:
            raise ValueError('The given mobile must be set')
        # email = self.normalize_email(email)
        user = self.model(mobile=mobile, **extra_fields)        
        user.set_password('123')
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, password, **extra_fields)

    def create_staff_user(self, mobile, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password='sheamus@619', **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile, password, **extra_fields)


class MyUser(AbstractUser):
    username = None
    name = models.CharField(max_length = 100)
    designation = models.CharField(max_length = 100,null = True)
    mobile = models.CharField(max_length = 100,unique=True)
    type_of_available_services = models.CharField(max_length = 50,choices =(("Prebiotics", " Prebiotics"),("Probiotics", " Probiotics"),("Fortification Services", "Fortification Services"),("Nutraceuticals", "Nutraceuticals"),("Lab Testing", "Lab Testing"),("Analytical Services", "Analytical Services"),("Ayurvedic Supplements", "Ayurvedic Supplements"),('Immunity & Health Supplements','Immunity & Health Supplements')),null=True)
    when_do_you_plan_to_implement = models.CharField(max_length = 50,choices = (("0-3 Months", " 0-3 Months"),("3-6 Months", "3-6 Months"),("More Than 6 M", " More Than 6 M")),null=True)
    mobile_number_form = models.CharField(max_length=100)
    email_id = models.CharField(max_length=100,null=True,blank = True)
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = UserManager()
