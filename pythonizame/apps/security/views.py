import sys
import logging
from urllib.request import urlopen

from django.shortcuts import render, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout
from django.utils.encoding import smart_str
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.views.generic import View
from django.template.loader import render_to_string

from pythonizame.apps.global_functions import format_sys_errors
from .forms import LoginForm, RegisterForm, RecoverPasswordForm, NewTokenForm, ChangePasswordForm
from .functions import send_email, get_url_gravatar
from .models import UserTokens
from pythonizame.core.json_settings import json_settings

settings = json_settings()

# Iniciamos el logger para estas vistas
logger = logging.getLogger(__name__)


class ChangePassword(View):
    template_name = 'cambiar_password.html'
    form = ChangePasswordForm

    def get(self, request, token, username):
        try:
            the_user = User.objects.get(username=username)
        except:
            raise Http404()
        try:
            my_token = UserTokens.objects.get(user=the_user, token=token)
        except:
            raise Http404()
        if the_user and my_token:
            return render(request, self.template_name, {'the_user': the_user,
                                                        'form': self.form})
        else:
            raise Http404()

    def post(self, request, token, username):
        form = self.form(request.POST)
        if form.is_valid():
            try:
                the_user = User.objects.get(username=username)
            except:
                the_user = None
            try:
                my_token = UserTokens.objects.get(user=the_user, token=token)
            except:
                raise Http404()
            if the_user and my_token:
                try:
                    the_user.set_password(form.cleaned_data['password_one'])
                    the_user.save()
                    my_token.delete()  # Eliminamos el token.
                    ctx = {'is_error': False, 'form': form, 'changed': True}
                except:
                    mensaje = format_sys_errors(sys, with_traceback=True)
                    logger.error(mensaje)
                    ctx = {'is_error': True, 'form': form, 'changed': False}
                return render(request, self.template_name, ctx)
            else:
                return Http404()
        else:
            ctx = {'is_error': True, 'form': form}
            return render(request, self.template_name, ctx)


class RecoverPassword(View):
    form = RecoverPasswordForm
    template_name = "recover_password.html"

    def get(self, request):
        ctx = {'form': self.form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']  # Obtenemos el email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user:
                # Creamos un token de cambio de contraseña
                UserTokens.objects.filter(user=user, type=1).delete()  # Eliminamos las anteriores.
                token = UserTokens()
                token.user = user
                token.type = 1  # Cambio de contraseña
                token.save()
                mensaje = smart_str("Hemos enviado un correo para que continúes "
                                    "con el proceso de recuperación de tu contraseña")
                # Ahora enviamos un email
                # Enviamos un correo de confirmacion
                to_email = user.email
                url_change_password = "%s/security/token/%s/password/%s/" % (
                    settings['URL_SERVER'], token.token, user.username)
                contenido = render_to_string("mail/password_change_template.html",
                                             {'url_change_password': url_change_password,
                                              'token': token.token,
                                              'user': user})
                send_email("Solicitud de cambio de contraseña", content=contenido, to=to_email,
                           content_type="text/html")
                sended = True
            else:
                sended = False
                mensaje = "No pudimos encontrar este email en nuestro sistema"
            ctx = {'message': mensaje, 'sended': sended, 'form': form}
            return render(request, self.template_name, ctx)
        else:
            ctx = {'message': 'Informacion no valida', 'form': form}
            return render(request, self.template_name, ctx)


class RegisterView(View):
    form = RegisterForm
    template_name = "register.html"
    welcome_template = "welcome.html"

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            ctx = {'form': self.form}
            return render(request, self.template_name, ctx)

    def post(self, request):
        from django.contrib.auth.models import User
        from pythonizame.apps.account.models import UserProfile
        from pythonizame.apps.account.lazymodels import LazyUserProfileData

        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                username = str(form.cleaned_data['username']).replace(" ", "")
                email = form.cleaned_data['email']
                password = form.cleaned_data['password_one']
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.is_active = False  # Inicialmente no está activado.
                new_user.save()
                # Ahora creamos su perfil
                lazy_data = LazyUserProfileData()
                lazy_data.country_code = form.cleaned_data['country_code']
                profile = UserProfile()
                profile.user = new_user
                profile.data = lazy_data.to_json()  # Guardamos los datos JSON
                # Generamos la imagen del gravatar
                url_gravatar = get_url_gravatar(email)
                image_stream = urlopen(url_gravatar)
                profile.image.save("img_{0}.jpg".format(profile.user.id), ContentFile(image_stream.read()))
                profile.save()
                # Ahora creamos un token para que active su cuenta
                token = UserTokens()
                token.user = new_user
                token.save()
                # Enviamos un correo de confirmacion
                to_email = new_user.email
                contenido = render_to_string("mail/activation_template.html", {'url_server': settings['URL_SERVER'],
                                                                               'token': token.token,
                                                                               'username': new_user.username,
                                                                               'password': password,
                                                                               })
                send_email("Bienvenido a Pythonízame", content=contenido, to=to_email, content_type="text/html")
                # Enviamos la vista para confirmar registro.
                ctx = {'is_registered': True, 'with_error': False}
                return render(request, self.template_name, ctx)
            except:
                mensaje = format_sys_errors(sys, with_traceback=True)
                ctx = {'with_error': True, 'form': form}
                return render(request, self.template_name, ctx)
        else:
            return render(request, self.template_name, {'form': form})


class Login(View):
    template_name = "login.html"
    form = LoginForm

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            ctx = {'form': self.form}
            return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            login(request, form.my_user)
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            ctx = {'form': form}
            return render(request, self.template_name, ctx)


class ActivateAccount(View):
    template_name = "activar_cuenta.html"

    def get(self, request, token):
        try:
            my_token = UserTokens.objects.get(token=token, type=0)
        except:
            my_token = False
        if my_token:
            user = my_token.user
            user.is_active = True
            user.save()
            my_token.delete()
            ctx = {'token_correcto': True}
        else:
            ctx = {'token_correcto': False}
        return render(request, self.template_name, ctx)


class RequestNewToken(View):
    template_name = "solicitar_token.html"
    form = NewTokenForm

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('security:login'))
        else:
            ctx = {'form': self.form}
            return render(request, self.template_name, ctx)

    def post(self, request):
        try:
            email = request.POST['email']
        except:
            email = None
        if email:
            try:
                user = User.objects.get(email=email)
            except:
                user = None
            if user:
                try:  # Si existe un token anterior entonces lo eliminamos.
                    UserTokens.objects.get(user=user, type=0).delete()
                except:
                    pass
                if user.is_active:
                    mensaje = "Tu usuario ya ha sido validado"
                else:
                    token = UserTokens()
                    token.user = user
                    token.save()
                    # Enviamos un correo de confirmacion
                    to_email = user.email
                    contenido = render_to_string("mail/new_token_template.html", {'url_server': settings['URL_SERVER'],
                                                                                  'token': token.token})
                    send_email("Solicitud de activación de cuenta", content=contenido, to=to_email,
                               content_type="text/html")
                    mensaje = "Hola! Generamos un nuevo Token y lo hemos enviado a tu correo electrónico. Gracias"
            else:
                mensaje = "No encontramos ningún registro con este email. ¿Eres un usuario nuevo?"
        else:
            mensaje = "Por favor, proporciona un email valido"
        ctx = {'mensaje': mensaje}
        return render(request, self.template_name, ctx)


class LogoutView(View):
    def get(self, request):
        """
        Vista tipo función que permite deslogearse del sistema.
        """
        logout(request)
        return HttpResponseRedirect(reverse('blog:index'))
