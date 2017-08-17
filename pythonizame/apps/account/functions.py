from urllib.request import urlopen

from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from pythonizame.apps.security.functions import get_url_gravatar
from .models import Achievement, UserAchievement, UserProfile


ID_LOGRO_FUNDADOR = 1
ID_LOGRO_300WARRIOR = 2


class CheckAchievements:
    """
    Este objeto nos permite identificar los logros de un usuario.
    Si tiene alguno pendiente por asignar, si ya tiene uno pero no lo ha visto,
    enviar logros pendientes por ver, enviar logros totales.
    """

    def __init__(self, my_user):
        self.__user = my_user

    def get_all_achievements(self):
        """
        Obtenemos todos los logros del usuario
        """
        return UserAchievement.objects.filter(user=self.__user)

    def get_all_pending_achievements(self):
        """
        Consultamos si el usuario tiene alguna medalla pendiente
        :return:
        """
        self.check_for_founder()  # Analizamos el logro fundador.
        self.check_for_300warrior()  # Analizamos el logro 300 guerreros.
        # Ahora consultamos los logros que tiene pendiente el usuario de ver.
        pending_achievements = UserAchievement.objects.filter(user=self.__user, viewed=False)
        return pending_achievements

    def check_for_founder(self):
        """
        Revisamos si el usuario es parte de los usuarios fundadores.
        Si es parte entonces consultamos si ya tiene el logro agregado o de lo contrario lo agregamos.
        """
        # Primero obtenemos el logro de fundador.
        try:
            logro = Achievement.objects.get(id=ID_LOGRO_FUNDADOR)
        except Achievement.DoesNotExist:
            logro = None
        if logro:  # Si existe el logro
            user_founders_id = User.objects.all().values_list('id', flat=True).order_by('id')[:logro.num_available]
            if self.__user.id in user_founders_id:
                # Si es fundador entonces revisamos si ya tiene el logro en la base de datos.
                UserAchievement.objects.get_or_create(user=self.__user, achievement=logro,
                                                      defaults={'user': self.__user, 'achievement': logro,
                                                                'date_received': timezone.now().date()})

    def check_for_300warrior(self):
        """
        Revisamos si el usuario es parte de los usuarios fundadores.
        Si es parte entonces consultamos si ya tiene el logro agregado o de lo contrario lo agregamos.
        """
        # Primero obtenemos el logro de fundador.
        try:
            logro = Achievement.objects.get(id=ID_LOGRO_300WARRIOR)
        except Achievement.DoesNotExist:
            logro = None
        if logro:  # Si existe el logro
            user_founders_id = User.objects.all().values_list('id', flat=True).order_by('id')[:logro.num_available]
            if self.__user.id in user_founders_id:
                # Si es fundador entonces revisamos si ya tiene el logro en la base de datos.
                UserAchievement.objects.get_or_create(user=self.__user, achievement=logro,
                                                      defaults={'user': self.__user, 'achievement': logro,
                                                                'date_received': timezone.now().date()})


def add_gravatar_if_empty_image(user):
    my_profile = UserProfile.objects.get(user=user)
    if my_profile.image:
        pass
    else:
        url_gravatar = get_url_gravatar(my_profile.user.email)
        image_stream = urlopen(url_gravatar)
        my_profile.image.save("img_{0}.jpg".format(my_profile.user.id), ContentFile(image_stream.read()))
        my_profile.save()
