from django.db import models
# Create your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.validators import RegexValidator
import pytz
from django.db.models.signals import post_init


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


class EmailSettings(models.Model):
    is_email_notifications_active = models.BooleanField(default=False)


class TextSettings(models.Model):
    is_text_notifications_active = models.BooleanField(default=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)  # Validators should be a list


class ExportSettings(models.Model):
    PDF = "pdf"
    TXT = "txt"
    CSV = "csv"
    EXPORT_CHOICES = [
        (PDF, "PDF"),
        (TXT, "TXT"),
        (CSV, "CSV"),
    ]
    export_format = models.CharField(max_length=3,
                                     choices=EXPORT_CHOICES,
                                     default=TXT)


class UserConfig(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(max_length=32, choices=TIMEZONES,
                                default='UTC')
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, primary_key=True)
    email_settings = models.OneToOneField(
        EmailSettings, on_delete=models.CASCADE)
    text_settings = models.OneToOneField(
        TextSettings, on_delete=models.CASCADE)
    export_settings = models.OneToOneField(
        ExportSettings, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not hasattr(self, "email_settings"):
            email_settings = EmailSettings()
            email_settings.save()
            self.email_settings = email_settings
            text_settings = TextSettings()
            text_settings.save()
            self.text_settings = text_settings
            export_settings = ExportSettings()
            export_settings.save()
            self.export_settings = export_settings
        super(UserConfig, self).save(*args, **kwargs)
