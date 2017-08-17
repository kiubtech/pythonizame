from django.conf.urls import url
from pythonizame.apps.account.webservices.views import ChangeImageProfile, UsernameValidation

app_name = "ws"

urlpatterns = [
    url(r'change/image_profile/$', ChangeImageProfile.as_view(), name='change_image_profile'),
    url(r'validate/username/$', UsernameValidation.as_view(), name='validate_username'),
]
