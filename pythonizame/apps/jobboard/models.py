from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django_countries.fields import CountryField


class JobCategory(models.Model):
    name = models.CharField(max_length=500, help_text=_("Nombre de la categoría del trabajo"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Categoría de empleo")
        verbose_name_plural = _("Categorías de empleo")


class Job(models.Model):
    SCHEDULE_CHOICES = (
        (1, _("Tiempo completo")),
        (0, _("Tiempo parcial"))
    )

    STATUS_TYPE = (
        (0, _("Rechazado")),
        (1, _("Aprobado")),
        (2, _("Borrador")),
        (3, _("En revisión")),
    )

    created_by = models.ForeignKey(User, verbose_name=_("Creado por"), help_text=_("Usuario que crea la vacante"))
    title = models.CharField(max_length=800, help_text=_("Título del trabajo"), verbose_name=_("Título"))
    description = models.TextField(max_length=2000, help_text=_("Describa de manera clara el puesto de trabajo"),
                                   verbose_name=_("Descripción"))
    categories = models.ManyToManyField(JobCategory, help_text=_("Categorías a la que aplica la vacante"),
                                        verbose_name=_("Categorías"))
    salary = models.CharField(max_length=600, help_text=_("Describe el salario a ofrecer por la vacante"),
                              verbose_name=_("Salario"))
    country = CountryField()
    address = models.CharField(max_length=500, null=True, blank=True, help_text=_("Ubicación del puesto"),
                               verbose_name=_("Dirección"))
    remote_working = models.BooleanField(default=False, help_text=_("¿Se acepta trabajo desde casa?"),
                                         verbose_name=_("Remoto"))
    work_schedule = models.IntegerField(choices=SCHEDULE_CHOICES, default=1, verbose_name=_("Horario"))
    # Información de la empresa.
    company_name = models.CharField(max_length=1000, help_text=_("Nombre de la empresa que propone la vacante"),
                                    verbose_name=_("Nombre de la empresa"))
    contact_email = models.CharField(max_length=1000, help_text=_("Email donde serán enviadas las aplicaciones"),
                                     verbose_name=_("Email de contacto"))
    website = models.URLField(null=True, blank=True, verbose_name=_("Sitio web"))
    status = models.IntegerField(choices=STATUS_TYPE, default=2)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))
    # Usuario que aprueba su autorización
    approval_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de aprobación"))
    approved_by = models.ForeignKey(User, related_name='approved_by', null=True, blank=True)
    num_of_views = models.IntegerField(default=0, help_text=_("Número de impresiones de tu job"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Empleo")
        verbose_name_plural = _("Empleos")
