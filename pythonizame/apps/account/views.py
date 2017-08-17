import logging
import sys
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from pythonizame.apps.account.functions import CheckAchievements

from pythonizame.apps.mixin import LoginRequiredMixin
from pythonizame.core.countries import COUNTRIES_JSON_LIST
from pythonizame.apps.global_functions import format_sys_errors
from .models import UserProfile, Power, UserAchievement
from .lazymodels import LazyUserProfileData

# Iniciamos el logger para estas vistas
logger = logging.getLogger(__name__)


class ChangePasswordView(LoginRequiredMixin, View):
    """
    Vista para cambiar contraseña del usuario
    """
    template_name = "change_password.html"

    def get(self, request):
        my_user = request.user
        if my_user:
            UserProfile.objects.get_or_create(user__username=my_user.username, defaults={'user': my_user})
            powers_id_list = my_user.userprofile.powers.all().values_list('id', flat=True)
            ctx = {'edit': False, 'my_powers_id': powers_id_list}
            return render(request, self.template_name, ctx)
        else:
            raise Http404

    def post(self, request):
        try:
            pass_one = request.POST['password_one']
            pass_two = request.POST['password_two']
            current = request.POST['current']
            if pass_one == pass_two:
                if request.user.check_password(current):  # Si es correcta su contraseña entonces cambiamos
                    if pass_one == current:
                        messages.error(request, "La actual no puede ser igual a la nueva contraseña")
                    else:
                        request.user.set_password(pass_one)  # Cambiamos el password.
                        request.user.save()
                        messages.success(request, 'Cambiado correctamente. Por favor ingresa de nuevo.')
                        # return HttpResponseRedirect(reverse('security:login'))
                else:
                    messages.error(request, 'La contraseña actual no coincide. Intenta de nuevo')
            else:
                messages.error(request, 'Las contraseñas ingresadas no coinciden')
        except:
            messages.error(request, 'Error en los datos recibidos')
        return render(request, self.template_name)


class ProfileView(View):
    """
    Vista para observar el perfil del usuario.
    """
    template_name = "profile.html"

    def get(self, request, user_id):
        try:  # Consultamos si lo enviado es un int
            user_id = int(user_id)
        except:  # De lo contrario enviamos a la página principal.
            return HttpResponseRedirect("/")
        the_user = get_object_or_404(User, id=user_id)  # obtenemos información del usuario
        UserProfile.objects.get_or_create(user__id=user_id,
                                          defaults={'user': the_user})  # Validamos si tiene perfil de usuario
        mis_logros = UserAchievement.objects.filter(user=the_user)
        my_context = {'edit': False, 'the_user': the_user, 'achievements': mis_logros}
        if self.request.user.is_authenticated():
            # Revisamos si tiene medallas pendientes.
            logros = CheckAchievements(self.request.user)
            logros_pendientes = logros.get_all_pending_achievements()
            if logros_pendientes:
                my_context['pending_achievements'] = logros_pendientes
                for logro in logros_pendientes:
                    logro.viewed = True
                    logro.date_received = timezone.now().date()
                    logro.save()
        return render(request, self.template_name, my_context)


class ProfileEditView(LoginRequiredMixin, View):
    """
    Vista para observar el perfil del usuario. Modo Edición.
    """
    template_name = "profile.html"

    def get(self, request, user_id):
        the_user = get_object_or_404(User, id=user_id)
        if the_user == request.user:
            userprofile, created = UserProfile.objects.get_or_create(user__id=user_id, defaults={'user': the_user})
            powers_id_list = userprofile.powers.all().values_list('id', flat=True)
            ctx = {'edit': True, 'countries': COUNTRIES_JSON_LIST,
                   'current_country': request.user.userprofile.country_code,
                   'powers': Power.objects.all().order_by('name'),
                   'my_powers_id': powers_id_list, 'the_user': the_user}
            return render(request, self.template_name, ctx)
        else:
            return HttpResponseRedirect("/account/%s/" % request.user.username)

    def post(self, request, user_id):
        if user_id == str(request.user.id):
            if 'powers_id' in request.POST:
                request.user.userprofile.powers.clear()
                arreglo = request.POST.getlist('powers_id')
                for my_id in arreglo:
                    power = Power.objects.get(id=my_id)
                    request.user.userprofile.powers.add(power)
            try:
                lazy_obj = LazyUserProfileData(request.POST)
                if 'first_name' in request.POST:
                    request.user.first_name = request.POST['first_name']
                    request.user.save()
                if 'about_me' in request.POST:
                    lazy_obj.about_me = request.POST['about_me']
                if 'website' in request.POST:
                    lazy_obj.website = request.POST['website']
                if 'about_me' in request.POST:
                    lazy_obj.about_me = request.POST['about_me']
                if 'country_code' in request.POST:
                    lazy_obj.country_code = request.POST['country_code']
                if 'twitter' in request.POST:
                    lazy_obj.twitter = request.POST['twitter']
                if 'facebook' in request.POST:
                    lazy_obj.facebook = request.POST['facebook']
                if 'github' in request.POST:
                    lazy_obj.github = request.POST['github']
                if 'gender' in request.POST:
                    lazy_obj.gender = request.POST['gender']
                if 'image' in request.FILES:
                    request.user.userprofile.image = request.FILES['image']
                request.user.userprofile.data = lazy_obj.to_json()
                request.user.userprofile.save()
                messages.success(request, 'Información actualizada correctamente')
                return HttpResponseRedirect(reverse('account:profile', args=(request.user.id,)))
            except:
                mensaje = format_sys_errors(sys, with_traceback=True)
                print(mensaje)
                messages.warning(request, 'Hubo un error, por favor intenta de nuevo.')
                ctx = {'edit': True}
        else:
            return HttpResponseRedirect(reverse('account:profile', args=(user_id,)))
        return render(request, self.template_name, ctx)
