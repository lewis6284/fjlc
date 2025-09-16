from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class Role(models.TextChoices):
    IT_MANAGER = "it_manager", "IT Manager"
    DIRECTOR = "director", "Director"
    CUSTOMER = "customer", "Customer"

class Religion(models.TextChoices):
    MUSLIM = "muslim", "Muslim"
    CHRISTIAN = "christian", "Christian"

class Gender(models.TextChoices):
    F = "female", "Female"
    M = "male", "Male"

# Minimal UserManager
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, telephone=None, password=None, role="customer", **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, full_name=full_name, telephone=telephone, role=role, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, telephone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, full_name, telephone, password, role="it_manager", **extra_fields)


class User(AbstractUser):
    username = None
    full_name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "telephone"]

    objects = UserManager()

    def __str__(self):
        return f"{self.full_name} ({self.role})"


class Post(models.Model):
      full_name = models.CharField(max_length=100)
      gender = models.CharField(max_length = 10, choices = Gender.choices, default=Gender.F)
      religion = models.CharField(max_length = 40, choices = Religion.choices, default=Religion.MUSLIM)
      cv = models.FileField(upload_to="cvs")
      video = models.FileField(upload_to="videos", null = True, blank = True)
      has_exp = models.BooleanField(default=False)
      is_taken = models.BooleanField(default=False)
      created_at=models.DateTimeField(auto_now_add=True,null=True)

      def __str__(self):
        return f"{self.full_name}"
