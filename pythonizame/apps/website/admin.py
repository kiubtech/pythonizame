from django import forms
from django.contrib import admin
from pythonizame.apps.website.models import FlatPage
from django.contrib.flatpages.models import FlatPage as FlatPageOriginal
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld
from django.contrib import admin

from solo.admin import SingletonModelAdmin
from ckeditor.widgets import CKEditorWidget

from .models import SiteConfiguration

admin.site.register(SiteConfiguration, SingletonModelAdmin)


class FlatpageForm(FlatpageFormOld):
    """
    Agregamos CKeditor a los flatpages de Django.
    """
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage  # this is not automatically inherited from FlatpageFormOld
        fields = '__all__'


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm
    fieldsets = (
            (None, {'fields': ('url', 'title', 'content', 'sites', 'status')}),
        )


# We have to unregister the normal admin, and then reregister ours
admin.site.unregister(FlatPageOriginal)
admin.site.register(FlatPage, FlatPageAdmin)
