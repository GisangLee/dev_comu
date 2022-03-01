import unicodedata
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password, make_password


class BaseManager(models.Manager):
    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        return email

    def make_random_password(
        self,
        length=10,
        allowed_chars="abcdefghjkmnpqrstuvwxyz" "ABCDEFGHJKLMNPQRSTUVWXYZ" "23456789",
    ):
        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """
        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class UserManager(BaseManager):
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

        superuser.is_superuser = True
        superuser.is_admin = True
        superuser.is_active = True
        superuser.is_staff = True

        superuser.set_password(password)
        superuser.save(using=self.db)
        return superuser


class User(models.Model):
    objects = UserManager()

    _password = None

    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"

    GENDER_CHOICES = ((GENDER_MALE, "Male"), (GENDER_FEMALE, "Female"))

    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(_("password"), max_length=128)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)
    login_try = models.PositiveIntegerField(default=0)
    email = models.EmailField(max_length=100)
    pwd_chg_date = models.DateField(blank=True, null=True)
    need_chg_pwd = models.BooleanField(default=False)
    is_dormant_account = models.BooleanField(default=False)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, max_length=10)
    is_wrong_pwd = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "email"

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )

    def update_last_login(sender, user, **kwargs):
        """
        A signal receiver which updates the last_login date for
        the user logging in.
        """
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.email


class UseProfile(models.Model):
    user = models.ForeignKey("User", related_name="profile", on_delete=models.CASCADE)
    file = models.ImageField(upload_to="profile/%Y/%m/%d", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = "user_profile"


class DormantUser(models.Model):
    user = models.ForeignKey("User", related_name="dormant", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_dormant"
