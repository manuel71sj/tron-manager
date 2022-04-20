from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# Create your models here.
from django.contrib.auth.models import _user_has_perm, PermissionsMixin, _user_has_module_perms
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, email, name, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        if not name:
            raise ValueError("Users must have an name")

        global_user_model = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = global_user_model.normalize_username(name)

        user = self.model(
            email=self.normalize_email(email),
            name=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, password, **extra_fields)

    def create_staff(self, email, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Staff must have is_staff=True.")

        return self._create_user(email, name, password, **extra_fields)

    def create_admin(self, email, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Admin must have is_staff=True.")
        if extra_fields.get('is_admin') is not True:
            raise ValueError("Admin must have is_admin=True.")

        return self._create_user(email, name, password, **extra_fields)

    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Admin must have is_staff=True.")
        if extra_fields.get('is_admin') is not True:
            raise ValueError("Admin must have is_admin=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Admin must have is_superuser=True.")

        return self._create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # _id = ObjectIdField()

    email = models.EmailField(
        _("email address"), max_length=255, unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    name = models.CharField(_("name"), max_length=150)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_admin = models.BooleanField(
        _("admin status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return '%s' % (self.email,)

    def get_full_name(self):
        return '%s (%s)' % (self.name, self.email)

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise, we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send email this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
