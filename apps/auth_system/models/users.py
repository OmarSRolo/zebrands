from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.misc.utils import validate_char_field


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name="", last_name="", town="", address="", phone="", city=""):
        if not email:
            raise ValueError(_('Users must have an email address'))

        user: Users = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.town = town
        user.city = city
        user.phone = phone
        user.address = address
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractUser):
    username = models.CharField(_('username'), max_length=150, unique=False, blank=True, null=True,
                                help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                error_messages={'unique': _("A user with that username already exists."), }, )
    email = models.EmailField(_('email address'), unique=True, validators=[validate_char_field])
    role = models.CharField(max_length=100, verbose_name="Role", null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono",
                             validators=[validate_char_field])
    address = models.CharField(max_length=250, blank=True, null=True, verbose_name="Dirección",
                               validators=[validate_char_field])
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ciudad",
                            validators=[validate_char_field])
    town = models.CharField(max_length=100, blank=True, null=True, verbose_name="Población",
                            validators=[validate_char_field])
    deleted_at = models.DateTimeField(verbose_name='Fecha de eliminación', blank=True, null=True)
    is_deleted = models.BooleanField(default=False, verbose_name='Eliminado')
    last_name = models.CharField(_('last name'), max_length=150, blank=True, null=True,
                                 validators=[validate_char_field])
    first_name = models.CharField(_("first name"), max_length=150, blank=True, validators=[validate_char_field])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    class Meta:
        verbose_name: str = "User"
        verbose_name_plural: str = "Users"
        db_table: str = "users"
