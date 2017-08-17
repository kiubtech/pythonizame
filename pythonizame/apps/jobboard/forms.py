from django import forms
from django.utils.translation import ugettext as _

from pythonizame.apps.jobboard.models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        exclude = ['created_by', 'approval_datetime', 'approved_by', 'status', 'num_of_views']
        labels = {
            "title": _("Título"),
            "description": _("Descripción"),
            "categories": _("Categorías"),
            "salary": _("Salario"),
            "country": _("País"),
            "address": _("Dirección"),
            "remote_working": _("¿Trabajo vía remota?"),
            "work_schedule": _("Horario"),
            "company_name": _("Nombre de la empresa"),
            "contact_email": _("Email de contacto"),
            "website": _("Sitio Web"),
        }
