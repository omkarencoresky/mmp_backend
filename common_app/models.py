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
    


class User_Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    house_no = models.CharField(max_length=20, blank=True, null=True)
    apartment = models.CharField(max_length=50, blank=True, null=True)
    nearest_landmark = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.CharField(max_length=200, blank=True, null=True)
    pin_code = models.CharField(max_length=20, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
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


class Permission(models.Model):

    PERMISSION_CHOICES = ['read', 'write', 'delete', 'update']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_id')
    permission = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permission_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permission_updated_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        """
        Ensure permissions are valid before saving.
        """
        permissions_list = self.permission.split(',')
        invalid_permissions = [
            perm for perm in permissions_list if perm.strip() not in self.PERMISSION_CHOICES
        ]
        if invalid_permissions:
            raise ValueError(f"Invalid permissions: {', '.join(invalid_permissions)}")
        self.permission = ','.join([perm.strip() for perm in permissions_list])
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'permission'


class Company(models.Model):
    COMPANY_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_user_id')
    company_name = models.CharField(max_length=255)
    company_email = models.EmailField(max_length=255)
    registration_number = models.CharField(max_length=50, unique=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    foundation_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    street_address = models.CharField(max_length=200, null=True, blank=True)
    pin_code = models.CharField(max_length=20, null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True, blank=True)
    company_status = models.CharField(max_length=10, choices=COMPANY_STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'companies'



class UserPermission(models.Model):

    permission_choices = [
        ('read', 'read'),
        ('write', 'write'),
        ('delete', 'delete'),
        ('update', 'update'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_permissions')
    granted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='granted_by_permissions')
    permission = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Ensure permissions are valid before saving.
        This method checks that each permission in the permission list
        is valid according to the permission_choices.
        """
        permissions_list = self.permission.split(',')
        
        invalid_permissions = [
            perm.strip() for perm in permissions_list if perm.strip() not in dict(self.permission_choices).keys()
        ]
        
        if invalid_permissions:
            raise ValueError(f"Invalid permissions: {', '.join(invalid_permissions)}")

        self.permission = ','.join([perm.strip() for perm in permissions_list])
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'user_permissions'