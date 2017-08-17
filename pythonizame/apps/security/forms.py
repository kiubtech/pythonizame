from django import forms
from django.contrib.auth.models import User
from pythonizame.core.countries import COUNTRIES_LIST


class ChangePasswordForm(forms.Form):
    password_one = forms.CharField(widget=forms.PasswordInput(attrs=({'class': 'validate form-control',
                                                                      'placeholder': 'Nueva contraseña',
                                                                      'required': 'required'})),
                                   required=True, label="")
    password_two = forms.CharField(widget=forms.PasswordInput(attrs=({'class': 'validate form-control',
                                                                      'placeholder': 'Repite tu nueva contraseña',
                                                                      'required': 'required'})),
                                   required=True, label="")

    def clean_password_two(self):
        if self.cleaned_data['password_one'] == self.cleaned_data['password_two']:
            pass
        else:
            raise forms.ValidationError("Contraseñas no coinciden, intente de nuevo.")


class RecoverPasswordForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs=({'class': 'validate form-control',
                                                            'placeholder': 'ingresa tu mail'})),
                            required=True, label="")


class RegisterForm(forms.Form):
    CHOICES = (('', 'Selecciona tu país'),) + COUNTRIES_LIST

    username = forms.CharField(widget=forms.TextInput(attrs=({'class': 'validate form-control',
                                                              'placeholder': 'Username', 'autocomplete': 'off'})),
                               required=True, label="")
    email = forms.EmailField(widget=forms.EmailInput(attrs=({'class': 'validate form-control', 'required': 'true',
                                                             'placeholder': 'Email'})),
                             required=True, label="")
    password_one = forms.CharField(widget=forms.PasswordInput(render_value=False,
                                                              attrs=({'class': 'validate form-control',
                                                                      'placeholder': 'Contraseña'})),
                                   required=True, label="")
    password_two = forms.CharField(widget=forms.PasswordInput(render_value=False,
                                                              attrs=({'class': 'validate form-control',
                                                                      'placeholder': 'Repite de nuevo tu contraseña '})),
                                   required=True, label="")
    country_code = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecciona tu país'}), choices=CHOICES,
        label="", required=True)

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
            raise forms.ValidationError("El nombre de usuario ya se encuentra ocupado")
        except User.DoesNotExist:
            return self.cleaned_data['username']

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError("Este email ya se encuentra registrado, has perdido tu contraseña?")
        except User.DoesNotExist:
            return self.cleaned_data['email']

    def clean_password_two(self):
        if self.cleaned_data['password_one'] == self.cleaned_data['password_two']:
            pass
        else:
            raise forms.ValidationError("Password no coincide, intente de nuevo")


class NewTokenForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs=({'class': 'validate form-control',
                                                            'placeholder': 'ingresa tu mail'})),
                            required=True, label="")


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs=({'class': 'form-control',
                                                              'placeholder': 'Username'})),
                               required=True, label="")
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs=({'class': 'form-control',
                                                                                      'placeholder': 'password'})),
                               required=True, label="")
    my_user = None  # Si se logea un usuario correctamente entonces se almacena aquí la sesión.

    def clean_password(self):
        from django.contrib.auth import authenticate
        # Primero verificamos si existe el usuario con el username enviado
        try:
            the_user = User.objects.get(username=self.cleaned_data['username'])
        except:
            the_user = None
        # Ahora intentamos encontrar al usuario con el email
        if not the_user:
            try:
                the_user = User.objects.get(email=self.cleaned_data['email'])
            except:
                the_user = None
        if the_user:
            user = authenticate(username=the_user.username,
                                password=self.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    self.my_user = user
                    pass
                else:
                    raise forms.ValidationError("Lo lamentamos, el usuario se encuentra deshabilitado")
            else:
                raise forms.ValidationError("Nombre de usuario y/o contraseña incorrecta")
        else:
            raise forms.ValidationError("Nombre de usuario y/o contraseña incorrecta")
