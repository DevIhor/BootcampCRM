from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, Permission, _user_get_permissions, _user_has_perm, _user_has_module_perms
from django.db import models
from django.utils.functional import cached_property


class UserManager(BaseUserManager):
    SUPERUSER_GROUPNAME = 'SuperAdmin'

    def create_user(self, email, password):
        """
        Creates and saves a User with the given email, date of birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_active = True
        user.groups.add(self.get_superuser_group())
        user.save()
        return user

    def create_superuser_group(self):
        """
        Creates and saves a superuser group with all basic permissions
        """
        superadmin_group, created = Group.objects.get_or_create(name=self.SUPERUSER_GROUPNAME)
        if created:
            permissions_list = Permission.objects.all()
            superadmin_group.permissions.set(permissions_list)
        return superadmin_group

    def get_superuser_group(self):
        """
        Returns a superuser group
        """
        superadmin_group, _ = Group.objects.get_or_create(name=self.SUPERUSER_GROUPNAME)
        return superadmin_group


class PermissionsMixin(models.Model):
    """
    Add the fields and methods necessary to support the Group and Permission models using the ModelBackend.
    """
    groups = models.ManyToManyField(
        Group, verbose_name='groups', blank=True, related_name="user_set", related_query_name="user",
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')
    user_permissions = models.ManyToManyField(
        Permission, verbose_name='user permissions', blank=True, related_name="user_set", related_query_name="user",
        help_text='Specific permissions for this user.')

    class Meta:
        abstract = True

    def get_user_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has directly
        """
        return _user_get_permissions(self, obj, 'user')

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their groups
        """
        return _user_get_permissions(self, obj, 'group')

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'all')

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission
        """
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        """
        return _user_has_module_perms(self, app_label)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(
        default=False, help_text='Designates whether this user has access to admin site.', verbose_name='is staff')
    is_active = models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this '
                                              'instead of deleting accounts.', default=False, verbose_name='is active')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
    password_change_date = models.DateTimeField(null=True, blank=True)
    last_login_date = models.DateTimeField(null=True, blank=True)
    last_activity_time = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @cached_property
    def is_superuser(self):
        supergroup = User.objects.get_superuser_group()
        return supergroup in self.groups.all()

    def __str__(self):
        return f"{self.id}, {self.email}"

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
