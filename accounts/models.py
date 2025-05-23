from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]


    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(regex=r'^09\d{9}$', message="شماره موبایل باید با 09 شروع شده و 11 رقم باشد.")
        ]
    )
    username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    gender = models.CharField(choices=GENDER_CHOICES ,max_length=10 ,blank=True ,null=True)
    author = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'age']


    def __str__(self):
        return f"{self.phone} - {self.full_name or 'کاربر'}"



    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-id']


class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
        ordering = ['-created_at']
        unique_together = ['from_user', 'to_user']

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username}"
