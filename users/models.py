from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_email_verified', True) 
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=128)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.email

class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(max_length=6)  # Adjust length based on your OTP requirements
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)  # To mark if OTP is used for verification

    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp_code}"

    # You can add custom methods, e.g., for validating the OTP if needed
    def is_valid(self):
        expiration_time = timezone.now() - self.created_at
        return not self.is_used and expiration_time.seconds < 300  # OTP is valid for 5 minutes
