from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_admin=False, is_active=False, is_staff=True):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError

        user = self.model(
            email=self.normalize_email(email)
        )
        user.admin = is_admin
        user.active = is_active
        user.staff = is_staff
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, is_admin=True, is_staff=False, is_active=True):
        user = self.create_user(
            email,
            password=password,
            is_staff=is_staff,
            is_admin=is_admin,
            is_active=is_active
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=100)
    admin = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='user_pics', default='images/default.png')

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

