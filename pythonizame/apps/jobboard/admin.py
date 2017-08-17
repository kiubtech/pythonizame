from django.contrib import admin, messages
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.utils import timezone
from .models import JobCategory, Job
from pythonizame.apps.security.functions import send_email


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'title', 'num_of_views', 'status')
    list_filter = ('status', 'timestamp', 'approval_datetime')
    filter_horizontal = ('categories', )
    search_fields = ['title', 'description']
    actions = ['approve_this', 'reject_this']
    readonly_fields = ('timestamp', 'approved_by', 'approval_datetime', 'num_of_views')

    def approve_this(self, request, queryset):
        if request.user.is_superuser or 'Administrador' in request.user.groups.values_list('name', flat=True):
            for obj in queryset:
                if not obj.status == 1:
                    obj.status = 1
                    obj.approved_by = request.user
                    obj.approval_datetime = timezone.now()
                    obj.save()
                    contenido = render_to_string("mail/job_approved_status.html",
                                                 {'job': obj})
                    send_email("Actualización de estatus de tu publicación", content=contenido, to=obj.created_by.email,
                               content_type="text/html")
                    message = _("Hemos aprobado este empleo")
                    messages.success(request, message)
                else:
                    message = _("Este Job ya ha sido aprobado anteriormente")
                    messages.warning(request, message)
        else:
            message = _("No cuentas con los permisos suficientes para ejecutar esta acción")
            messages.error(request, message)

    approve_this.label = _("Aprobar job(s)")  # optional
    approve_this.short_description = _("Aprobar job(s)")  # optional

    def reject_this(self, request, queryset):
        if request.user.is_superuser or 'Administrador' in request.user.groups.values_list('name', flat=True):
            for obj in queryset:
                if not obj.status == 0:
                    obj.status = 0
                    obj.save()
                    contenido = render_to_string("mail/job_rejected_status.html",
                                                 {'job': obj})
                    send_email("Actualización de estatus de tu publicación", content=contenido, to=obj.created_by.email,
                               content_type="text/html")
                    message = _("Hemos rechazado este empleo")
                    messages.success(request, message)
                else:
                    message = _("Este empleo ya se encuentra rechazado")
                    messages.warning(request, message)
        else:
            message = _("No cuentas con los permisos suficientes para ejecutar esta acción")
            messages.error(request, message)

    reject_this.label = _("Rechazar job(s)")  # optional
    reject_this.short_description = _("Rechazar job(s)")  # optional
