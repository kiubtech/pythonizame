from django.conf.urls import url, include
from pythonizame.apps.account.views import ProfileView, ProfileEditView, ChangePasswordView


app_name = "account"


urlpatterns = [
    url(r'^ws/', include('pythonizame.apps.account.webservices.urls')),
]

urlpatterns += [
    url(r'change/password/$', ChangePasswordView.as_view(), name="change_password"),
    url(r'^(?P<user_id>\w+)/$', ProfileView.as_view(), name="profile"),
    url(r'^(?P<user_id>\w+)/edit/$', ProfileEditView.as_view(), name="profile_edit"),
]
