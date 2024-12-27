import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password



class User(models.Model):
    ROLE_CHOICES = {
        'user': 'user',
        'driver': 'driver',
        'travel_admin': 'travel_admin',
        'package_admin': 'package_admin',
        'travel_sub_admin': 'travel_sub_admin',
        'package_sub_admin': 'package_sub_admin',
    }

    GENDER = {
        'male': 'male',
        'other': 'other',
        'female': 'female',
    }

    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    phone_no = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=50, choices=GENDER)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    profile_url = models.URLField(max_length=200, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')
    creator_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_no', 'first_name', 'last_name', 'password']


    class Meta:
        db_table = 'users'


    def save(self, *args, **kwargs):
        """
        Make the user password hashed and saved it.
        """
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


    def check_password(self, raw_password):
        """
        Check if the provided raw_password matches the hashed password stored in the database.
        """
        return check_password(raw_password, self.password)
    
    def get_username(self):
        """
        Return the username used for authentication, which is 'email' in this case.
        """
        return self.email


class User_Address(models.Model):
    id = models.AutoField(primary_key=True)
    user_id =models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=20, blank=True, null=True)
    street_address = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_address'

    
class OAuthApplication(models.Model):
    name = models.CharField(max_length=255)
    client_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client_secret = models.UUIDField(default=uuid.uuid4, editable=False)
    redirect_uris = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oauth_application'

    def __str__(self):
        return self.name

class OAuthAccessToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    application = models.ForeignKey(OAuthApplication, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expires_at = models.DateTimeField()
    scope = models.TextField(default='read write')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oauth_access_token'

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"{self.user.username} - {self.application.name}"

class OAuthRefreshToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    access_token = models.OneToOneField(OAuthAccessToken, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'oauth_refresh_token'