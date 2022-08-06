from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, **extra_fields):
        try:
            user = self.model(
                email=self.normalize_email(email), username=username, **extra_fields
            )
            return user
        except Exception as e:
            print("CREATE USER ERROR : ", e)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            username=username, email=self.normalize_email(email)
        )

        superuser.is_admin = True

        superuser.set_password(password)
        superuser.save(using=self.db)
        return superuser


class User(AbstractBaseUser):
    objects = UserManager()

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"

    LOGIN_KAKAO = "kakao"
    LOGIN_GOOGLE = "google"
    LOGIN_EMAIL = "email"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "email"),
        (LOGIN_GOOGLE, "google"),
        (LOGIN_KAKAO, "kakao"),
    )

    GENDER_CHOICES = ((GENDER_MALE, "M"), (GENDER_FEMALE, "F"))

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, max_length=10)
    login_method = models.CharField(choices=LOGIN_CHOICES, max_length=6, default=LOGIN_EMAIL)
    is_admin = models.BooleanField(default=False)
    birthdate = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email_secret = models.TextField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        # return self.is_admin
        return True

    def has_perm(self, perm, obj=None):
        # return self.is_admin
        return True

    class Meta:
        db_table = "accounts"


class UserProfile(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="profile_images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "profile_images"