from django.conf.urls import *
from .views import Login, RegisterView, ActivateAccount, RequestNewToken, RecoverPassword, ChangePassword, LogoutView

urlpatterns = [
    url(r'^login/$', Login.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'activation/(?P<token>.*)/$', ActivateAccount.as_view(), name='activation_account'),
    url(r'token/(?P<token>.*)/password/(?P<username>.*)/$', ChangePassword.as_view(), name='change_password'),
    url(r'new/token/activation/$', RequestNewToken.as_view(), name='new_token_activation'),
    url(r'recover/password/$', RecoverPassword.as_view(), name='recover_password'),
]
