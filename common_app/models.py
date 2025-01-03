import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Role(models.Model):
    """
    Model representing a role with a unique ID, name, description,
    and timestamps for creation and updates.
    """
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=100,unique=True,null=False)
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'roles'



class User(models.Model):

    GENDER_CHOICES = {
        'male': 'male',
        'other': 'other',
        'female': 'female',
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users_role_id')
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_no = models.CharField(max_length=15, unique=True)
    country_code = models.CharField(max_length=10, default='+1')
    profile_url = models.URLField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)    
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
    
    def get_user_by_idname(self):
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
    id = models.AutoField(primary_key=True)
    client_id = models.CharField(max_length=255, unique=True)
    client_secret = models.CharField(max_length=255)
    redirect_uri = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'oauth_application'


class OAuthAccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(OAuthApplication, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, unique=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    token_type = models.CharField(max_length=50)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oauth_access_token'