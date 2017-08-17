from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from pythonizame.apps.global_functions import get_cleaned_uuid


def one_day_hence():
    return timezone.now() + timezone.timedelta(days=10)


class UserTokens(models.Model):

    TOKEN_TYPE = (
        (0, 'Activación de cuenta'),
        (1, 'Cambiar contraseña'),
    )
    token = models.CharField(max_length=100, primary_key=True, default=get_cleaned_uuid, editable=False)
    type = models.IntegerField(choices=TOKEN_TYPE, default=0)
    user = models.ForeignKey(User)
    expiration_date = models.DateTimeField(default=one_day_hence, null=True, blank=True)

    def __str__(self):
        return self.token

    class Meta:
        unique_together = ('user', 'type')
        verbose_name = "Tokens de seguridad"
        verbose_name_plural = "Tokens de seguridad"
