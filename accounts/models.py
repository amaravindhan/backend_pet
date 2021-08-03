from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        """Creates and saves a new staff user"""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using phone number instead of username"""

    userTypeChoices = [
            ('pet_owner', 'Pet Owner'), ('care_taker', 'Care Taker'), 
            ('vet_doctor', 'Doctor'), ('store_owner', 'Store Owner'), 
            ('store_staff', 'Store Staff')
        ]

    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,13}$',
                                 message="Phone Number must be 10 digits!")
    phone_number = models.CharField(_("Phone Number"), max_length=13,
                                    validators=[phone_regex], unique=True)
    email = models.EmailField(max_length=255, unique=True, null=True)
    username = models.CharField(
        _("Username"), max_length=50, unique=True, null=True)

    full_name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=50, choices=userTypeChoices, default='pet_owner')

    is_phone_verified = models.BooleanField(default=False, _('Phone Verified'))
    is_email_verified = models.BooleanField(default=False, _('Email Verified'))

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_number'
    # REQUIRED_FIELDS = ['organization']

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username

    def __str__(self):
        return self.phone_number
